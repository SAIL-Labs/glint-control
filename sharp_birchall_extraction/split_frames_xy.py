# Reads in frames and splits them into sections, based on the divisions in y

import glob
import astropy.io.fits as fits
import matplotlib.pyplot as plt
import ipdb
import numpy as np

# directory containing frames to split
dir_read = '/home/scexao/eckhart/spectral_extraction_test_20240927/data/individual_slices/'

file_names = glob.glob(dir_read + '*.fits')

# at what y-values should frames be split? (include 0 and -1)
splits_in_y = [0,20,40,70,-1]

for file_num in range(0,len(file_names)):

    # Read in the first FITS file
    with fits.open(file_names[file_num]) as hdul:
        data = hdul[0].data
        header = hdul[0].header

        for split_num in range(len(splits_in_y)-1):

            data_string = 'data_' + str(split_num)
            
            if len(np.shape(data))==2:
                data_section = data[splits_in_y[split_num]:splits_in_y[split_num+1],:]
            elif len(np.shape(data))==3:
                data_section = data[:,splits_in_y[split_num]:splits_in_y[split_num+1],:]
            print('------')
            print(split_num)
            print(split_num+1)

            #plt.clf()
            #plt.imshow(data_section)
            #plt.show()

            split_file_name = f"{file_names[file_num][:-5]}_split_{split_num}.fits"
            ipdb.set_trace()
            fits.writeto(split_file_name, data_section, header, overwrite=True)
            print('Wrote',split_file_name)

        # Save the split data to a new FITS file
        #split_file_name = f"{file_names[file_num][:-5]}_split_{i}.fits"
        #fits.writeto(split_file_name, split_data, split_header, overwrite=True)