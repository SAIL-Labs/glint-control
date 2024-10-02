import matplotlib.pyplot as plt
import numpy as np
from utils import fcns, backbone_classes
import time
import os
import configparser
from configparser import ExtendedInterpolation
from astropy.io import fits
import glob
import image_registration
from image_registration import chi2_shift
from image_registration.fft_tools import shift
from astropy.convolution import interpolate_replace_nans
import json
import time
import ipdb
import cProfile
import warnings

## ## TBD: make clearer distinction between length of spectra, and that of extraction profile

def main(config_file):

    # silence some warnings
    os.environ['MKL_DEBUG_CPU_TYPE'] = '5'
    warnings.filterwarnings("ignore")

    # Read the config file
    config = configparser.ConfigParser(interpolation=ExtendedInterpolation())
    config.read(config_file)

    # make wavelength mapping?
    wavel_map = config['options']['WAVEL_MAP']

    if wavel_map == '1':
        # read wavelength solution file (as set by config file)
        with open(config['file_names']['FILE_NAME_WAVEL_PARAMS'], 'r') as file:
            wavel_data = json.load(file)
    elif wavel_map == '0':
        print('No wavelength solution being made')

    # make directories if they don't exist yet
    [os.makedirs(value, exist_ok=True) for value in config['sys_dirs'].values()]

    # generate spectral profiles: either by 
    # 1. generating a simple horizontal profile for each spectrum (profiles_file_name = None), or
    # 2. reading in a profiles cube from file
    if config['options']['PROFILE_SOURCE'] == 'simple':
        simple_profiles_config_file = config['file_names']['FILE_NAME_SIMPLE_PROFILES_CONFIG']
        profiles_file_name = None
    elif config['options']['PROFILE_SOURCE'] == 'from_file':
        simple_profiles_config_file = None
        profiles_file_name = config['file_names']['FILE_NAME_PROFILES']
    profiles = fcns.stacked_profiles(simple_profiles_config_file, profiles_file_name)
    # find the individual x, y coordinates along the spectra based on the profiles
    x_coords_spectra_true, y_coords_spectra_true = fcns.find_xy_spectra(profiles = profiles)
    
    # directory containing readouts to extract
    dir_spectra_parent = config['sys_dirs']['DIR_DATA']
    # Glob the directories inside the specified directory
    dir_spectra_read = glob.glob(dir_spectra_parent + '*series*/')
    # directory to which we will write spectral solutions
    dir_spectra_write = config['sys_dirs']['DIR_WRITE']

    # retrieve a bad pixel mask (should be in correct rotation orientation)
    badpix_mask = fits.open(config['file_names']['FILE_NAME_BADPIX'])[0].data

    # a sample frame (to get dims etc.)
    test_frame = fcns.read_fits_file(config['file_names']['FILE_NAME_SAMPLE'])
    if len(np.shape(test_frame)) > 2:
        test_data_slice = test_frame[0,:,:]
    else:
        test_data_slice = test_frame

    # retrieve a variance image
    # (do not fix bad pixels! causes math to fail)
    readout_variance = fits.open(config['file_names']['FILE_NAME_VAR'])[0].data
    readout_variance[readout_variance == 0] = np.nanmedian(readout_variance) # replace 0.0 pixels (since this will lead to infs later)
    readout_variance[readout_variance < 0] = np.nanmedian(readout_variance)
    # do the images have to be rotated?
    if (config['options']['ROT_LEFT'] == '1'): 
        test_data_slice = np.rot90(test_data_slice, k=3)
        readout_variance = np.rot90(readout_variance, k=3)

    # calculate the things that will be needed when extracting spectra from individual readouts
    spec_extraction = backbone_classes.Extractor(num_spec=len(profiles), 
                                                 len_spec=np.shape(test_data_slice)[1], 
                                                 sample_frame=test_data_slice,
                                                 dict_profiles=profiles, 
                                                 array_variance=readout_variance, 
                                                 n_rd=0)

    # fake data for quick checks: uncomment this section to get spectra which are the same as the profiles
    '''
    test_frame = fcns.read_fits_file('test_array.fits')
    test_data_slice = test_frame
    test_variance_slice = np.sqrt(test_data_slice)
    # insert some noise
    test_data_slice += (1e-3)*np.random.rand(np.shape(test_data_slice)[0],np.shape(test_data_slice)[1])
    test_variance_slice += (1e-3)*np.random.rand(np.shape(test_variance_slice)[0],np.shape(test_variance_slice)[1])
    '''

    if wavel_map == '1':
        # guesses of (x,y) of sampled spots
        # {"[spec number]": {"x_guesses": [x1, x2, x3, ...], "y_guesses": [y1, y2, y3, ...]
        # {"wavel_array": [wavelength_nm, wavelength_nm, ...]}
        xy_guesses_basis_set = wavel_data['xy_guesses_basis_set'] # array of spots corresponding to narrowband spots
        # sampled wavelengths 
        # {"wavel_array": [wavelength_nm, wavelength_nm, ...]}
        wavel_array = wavel_data['wavel_array'] # array of sampled wavelengths

        # generate the basis wavelength solution
        # xy_pix_locs = (x_coords_spectra_true, y_coords_spectra_true)
        wavel_gen_obj = backbone_classes.GenWavelSoln(num_spec = len(profiles), 
                                                    dir_read = config['sys_dirs']['DIR_PARAMS_DATA'], 
                                                    wavel_array = np.array(wavel_array), 
                                                    xy_narrowband_spot_guesses = xy_guesses_basis_set)

        basis_cube = wavel_gen_obj.read_basis_cube(file_name = config['file_names']['FILE_NAME_WAVEL_BASIS_CUBE'])

        # find (x,y) of narrowband (i.e., point-like) spectra in each frame of basis cube
        wavel_gen_obj.find_xy_narrowbands(xy_guesses = xy_guesses_basis_set,
                                        basis_cube = basis_cube)
        
        # generate solution coefficients
        wavel_gen_obj.gen_coeffs(target_instance = wavel_gen_obj)

        # read in a lamp basis image (to find x,y-offsets later)
        wavel_gen_obj.add_basis_image(file_name = config['file_names']['FILE_NAME_BASISLAMP'])


    '''
    if (config['options']['ROT_LEFT'] == '1'): wavel_gen_obj.lamp_basis_frame = np.rot90(wavel_gen_obj.lamp_basis_frame, k=3)
    '''

    '''
    # retrieve lamp image
    lamp_file_name = glob.glob(config['file_names']['FILE_NAME_THISLAMP'])
    lamp_data = fits.open(lamp_file_name[0]) # list of files should just have one element
    lamp_array_this = lamp_data[0].data[0,:,:]
    lamp_array_this = fcns.fix_bad(array_pass=lamp_array_this, badpix_pass=badpix_mask) # fix bad pixels

    # rotate image CCW? (to get spectra along x-axis)
    if (config['options']['ROT_LEFT'] == '1'): lamp_array_this = np.rot90(lamp_array_this, k=3)
    '''

    if (config['options']['ROT_LEFT'] == '1'): readout_variance = np.rot90(readout_variance, k=3)

    # find offset from lamp basis image
    '''
    # removed temporarily to get pipeline to work on simple dataset
    xoff, yoff, exoff, eyoff = chi2_shift(wavel_gen_obj.lamp_basis_frame, lamp_array_this)
    '''
    
    # Get the initial list of files in the directory
    initial_files = os.listdir(dir_spectra_parent)


    # Start monitoring the directory for files
    #while True:
        
    if (config['options']['WHICH_FILES'] == 'new'):
        # the new files that have appeared
        current_files = os.listdir(dir_spectra_parent)
        list_files = [file for file in current_files if file not in initial_files]
        print('This new mode needs to be debugged, as the code structure has changed')
        ipdb.set_trace()
    elif (config['options']['WHICH_FILES'] == 'all'):
        # all pre-existing files
        list_files = glob.glob(dir_spectra_parent + "*.fits")


    # Process the new files
    for file in list_files:

        start_time = time.time()

        # Construct the full path to the file
        file_path = os.path.join(dir_spectra_parent, file)

        # read in image
        hdul = fits.open(file_path)

        if len(np.shape(hdul[0].data)) > 2:
            if (config['options']['WHICH_SLICE'] == '0'):
                readout_data = hdul[0].data[0,:,:]
        else:
            readout_data = hdul[0].data

        # some ad hoc bad pix fixing ## ## TODO: make better badpix mask
        readout_data[readout_data<0] = 0
        readout_data = fcns.fix_bad(array_pass=readout_data, badpix_pass=badpix_mask)
        readout_data[readout_data < 0] = np.nanmedian(readout_data)

        # rotate image CCW? (to get spectra along x-axis)
        if (config['options']['ROT_LEFT'] == '1'): readout_data = np.rot90(readout_data, k=3)

        # translate the image to align it with the basis lamp (i.e., with the wavelength solns)
        '''
        readout_data = shift.shiftnd(readout_data, (-yoff, -xoff))
        readout_variance = shift.shiftnd(readout_variance, (-yoff, -xoff))
        '''

        # initialize basic spectrum object which contains info specific to this spectrum
        spec_obj = backbone_classes.OneSpecData(num_spec = len(profiles), 
                                            sample_frame = test_data_slice, 
                                            profiles = profiles)

        # do the actual spectral extraction, and update the spec_obj with them
        spec_extraction.extract_one_frame(target_instance=spec_obj, 
                                            D=readout_data, 
                                            process_method = config['options']['PROCESS_METHOD'], 
                                            fyi_plot=False)

        if wavel_map == '1':
            # apply the wavelength solution

            fcns.apply_wavel_solns(num_spec = len(profiles), 
                                    x_vals_spectra = x_coords_spectra_true, 
                                    y_vals_spectra = y_coords_spectra_true,
                                source_instance = wavel_gen_obj, 
                                target_instance = spec_obj)

        # write to file
        file_name_write = dir_spectra_write + 'extracted_' + os.path.basename(file_path)
        fcns.write_to_file(target_instance=spec_obj, file_write = file_name_write)

        end_time = time.time()
        execution_time = end_time - start_time
        print("Execution time total:", execution_time, "seconds")

        # make FYI plots of extracted spectra
        # loop over all spectra on that detector frame
        if (config['options']['WRITE_PLOTS'] == '1'):

            plt.clf()
            # loop over the spectra which appear simultaneously on the arrays
            for i in range(0,len(spec_obj.spec_flux)):

                # for graph scale (TBD)
                '''
                if i==0:
                    graph_extent = np.std()
                '''

                # plot the spectra
                file_name_plot = config['sys_dirs']['DIR_WRITE_FYI'] + os.path.basename(file_path).split('.')[0] + '.png'
                if (config['options']['WAVEL_MAP'] == '1'):
                    plt.plot(spec_obj.wavel_mapped[str(i)], spec_obj.spec_flux[str(i)]+3000*i, label='flux')
                    #plt.plot(spec_obj.wavel_mapped[str(i)], np.sqrt(spec_obj.vark[str(i)]), label='$\sqrt{\sigma^{2}}$')
                elif (config['options']['WAVEL_MAP'] == '0'):
                    plt.plot(spec_obj.spec_flux[str(i)]+50000*i, label='flux')
                    #plt.plot(np.sqrt(spec_obj.vark[str(i)]), label='$\sqrt{\sigma^{2}}$')
                #plt.legend()
            #plt.ylim([-100,45000])
            plt.savefig( file_name_plot )
            print('Wrote',file_name_plot)

    '''
    # Update the initial list of files
    if (config['options']['WHICH_FILES'] == 'new'):
        initial_files = current_files

    # Wait for some time before checking again
    time.sleep(1)
    '''

if __name__ == "__main__":
    #cProfile.run('main()', 'profile_stats.prof')

    stem = './' # put in absolute stem here
    #main(config_file = stem + 'config_eckhart_superk_glint_20240927_cred1.ini') # 12 channel GLINT data of SuperK source
    main(config_file = stem + 'config_yoo_jung_smf_superk_20240110.ini') # 1 channel, SMF super-K source
    #main(config_file = stem + 'config_yoo_jung_altair_20240818_cred2.ini') # 12 channel GLINT data, with wavelength solution
    #main(config_file = stem + 'config_yoo_jung_3PL.ini') # 3PL data, with wavelength solution
    #main(config_file = stem + 'config_12_channel_cred2.ini') # 12 channel GLINT data, with wavelength solution
    #main(config_file = stem + 'config_fake_seeing_20240509.ini') # 3 channel PL data with fake seeing, without wavelength solution