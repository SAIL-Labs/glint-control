"""
The main class to handle controlling the GLINT instrument.
Eventually this will be wrapped in a GUI!
"""

import numpy as np
import matplotlib.pyplot as plt
plt.ion()

class glintcontrol:
    def __init__(self, datapath):
        self.datapath = datapath # Need to specify path to save and read data (incl. config files)
                                 # In future, can separate into different directories based on type

        # Define chip input space
        self.input_wgs = np.array([1, 2, 3]) # Input WG numbering
        self.input_segs = np.array([6, 9, 17])  # Corresponding MEMS seg numbers
        self.baselines = np.array([[1, 2], [2, 3], [1, 3]]) # Baseline numbering

        # Define chip output space
        self.output_wgs = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]) # Output WG numbering
        self.output_wg_labels = ['P1', 'B1A', 'N1', 'B1B', 'P2', 'B2A', 'N2',
                                 'B2B', 'P3', 'B3A', 'N3', 'B3B', ]

        # Store spectral channel info
        self.wl_px = None # Vector of x pixel positions for each WL channel
        self.wl_channels = None # Vector of wavelengths for each WL channel (microns)

        # Store MEMS, actuator positions, etc. as instance variables.
        # Address only used segments
        self.mems_seg_tts = None # Current positions (mrad)
        self.mems_seg_pists = None # microns
        self.mems_seg_tts_opt = None # mrad
        self.mems_seg_pists_opt = None # microns

        # For now, store data (i.e. camera images, spectra) as instance variables.
        # Later these could become tehir own objects
        self.current_camera_frame = None
        self.current_flux_vectors = None # Shape [output_chans, wavelengths]
        self.darkframe = None # The current darkframe to subtract before extracting fluxes


    def get_latest_camera_frame(self, subtract_dark=True):
        ### STUB
        # Get the latest camera frame, subtract self.darkframe is requested, and store in
        # self.current_camera_frame.
        pass


    def get_darkframe(self, nframes=1, save_to_file=True, datapath=None, filepref=None):
        ### STUB
        # Set the latest nframes frames from the camera, average them, and set as self.darkframe.
        # Save the darkframe to a file if requested, to specified datapath and/or file prefix
        # if provided (see self.save_test_data() for more info).
        pass


    def get_latest_fluxes(self):
        ### STUB
        # Extract the flux vectors from self.current_camera_frame
        n_outputs = self.output_wgs.shape[0]
        n_wls = self.wl_channels.shape[0]
        self.current_flux_vectors = np.zeros((n_outputs, n_wls))
        pass


    def set_MEMS_posns(self, input_wgs, cmd_posns):
        ### STUB
        # Sets the segment(s) corresponding to input_wg(s) to the given tip, tilt & piston values
        # cmd_posns is an nx3 array of form  [[tip, tilt, piston]], where n=len(input_wgs).
        # Then update self.mems_seg_tts and self.mems_seg_pists with the new values.
        # If an element in cmd_posns is None, leave the corresponding tip/tilt/piston position unchanged
        pass


    def mems_tiptilt_scan(self, input_wg, scanlims=(-3, 3, -3, 3), showplot=False):
        ### STUB
        # Performs an injection optimisation scan for the requested input_wg via tip/tilt of the
        # corresponding MEMS segment, over the range given by scanlims. A function (such as a 2D
        # Gaussian) is fitted to the raster-scanned values to find the true optimum.
        # When the optimum is found, set the MEMS to this position and store the result in
        # self.mems_seg_tts_opt. Also display an image/plot of the fit if requested.
        pass


    def mems_piston_scan(self, input_wgs, seg2pist=0, scanlims=(-3, 3), showplot=False):
        ### STUB
        # Performs a null-depth optimisation scan for the requested baseline via piston of the
        # corresponding MEMS segments, over the range given by scanlims. Each baseline has 2 segments -
        # which of these is pistoned is determined by seg2pist, which is either 0 or 1.
        # A function (such as a sinc function) is fitted to the scanned values to find the true optimum.
        # When the optimum is found, set the MEMS to this position and store the result in
        # self.mems_seg_pists_opt. Also display an image/plot of the fit if requested.
        pass


    def save_test_data(self, nframes=1, datapath=None, filepref=None, save_raw_ims=False):
        ### STUB
        # Do a _slow_ save of nframes of extracted fluxes, and the raw camera frames if requested.
        # This is not realtime, so will miss many frames, so is just for testing and diagnostics.
        # npz format is probably best for now

        if datapath is None:
            datapath = self.datapath

        if filepref is None:
            # Automatically assign a file prefix based on date/time, etc.
            pass

        pass


    def sim_chip(self, 
                 input_complex_wavefronts = [1., 0., 1., 0., 1., 0.], 
                 phase_shifts_aps = (2.*np.pi/3.)*np.ones(3), 
                 splitting_coeffs_photom = 0.2, 
                 splitting_coeffs_interf = [0.4, 0.6, 0.5, 0.5, 0.3, 0.7]):

        ##################################
        ## start inputs

        # parameters of incoming complex wavefronts, before any splitting [units radians]
        # (note these are upstream of the achromatic phase shift; these phases are NOT from the APSes)
        amp_I, phase_I, amp_II, phase_II, amp_III, phase_III = input_complex_wavefronts

        # phase shifts induced by APSes in waveguides; assumed achromatic; 120 deg = 2*pi/3
        phase_shift_1, phase_shift_2, phase_shift_3  = phase_shifts_aps

        # splitting coefficient of that going into photometric tap at each such split (values for waveguides 1 and 2 assumed the same)
        ## ## TO DO: allow for 3 different alpha vals
        ## ## TO DO: reduce other vals to x, 1-x pairs
        alpha_val = splitting_coeffs_photom
        # splitting coefficients just before coupling stage (note that certain pairs have to sum to 1, assuming no energy loss)
        beta_val, gamma_val, delta_val, omega_val, eta_val, sigma_val  = splitting_coeffs_interf

        ## end inputs
        ##################################

        # input wavefonts
        phasor_in_I = amp_I * np.exp(1j * phase_I)
        phasor_in_II = amp_II * np.exp(1j * phase_II)
        phasor_in_III = amp_III * np.exp(1j * phase_III)
        a_in = np.array([phasor_in_I, phasor_in_II, phasor_in_III])

        # phasors for APSes
        phase_term_1 = np.exp(1j * phase_shift_1)
        phase_term_2 = np.exp(1j * phase_shift_2)
        phase_term_3 = np.exp(1j * phase_shift_3)

        # transfer matrix of photometric splitting
        M_phot = np.array([[1 - alpha_val,         0,               0], 
                        [0,                     1 - alpha_val,               0],
                        [0,                     0,              1 - alpha_val],
                        [alpha_val,             0,              0],
                        [0,             alpha_val,              0],
                        [0,                     0,              alpha_val]])

        # transfer matrix of interferometric splitting
        M_interf = np.array([[beta_val,      0,      0,      0,      0,      0], 
                        [0,      0,      0,      0,      0,      0], 
                        [0,      delta_val,      0,      0,      0,      0], 
                        [0,      omega_val,      0,      0,      0,      0], 
                        [0,      0,      0,      0,      0,      0], 
                        [0,      0,      eta_val,      0,      0,      0],
                        [gamma_val,      0,      0,      0,      0,      0],
                        [0,      0,      0,      0,      0,      0],
                        [0,      0,      sigma_val,      0,      0,      0],
                        [0,      0,      0,      1,      0,      0],
                        [0,      0,      0,      0,      1,      0],
                        [0,      0,      0,      0,      0,      1]])

        # achromatic phase shifters, now arranged as a matrix
        aps_1_phasor = np.exp(1j * phase_shift_1)
        aps_2_phasor = np.exp(1j * phase_shift_2)
        aps_3_phasor = np.exp(1j * phase_shift_3)

        P_aps = np.array([[1,      0,      0,      0,      0,      0,    0,      0,      0,      0,      0,      0], 
                    [0,      1,      0,      0,      0,      0,    0,      0,      0,      0,      0,      0],
                    [0,      0,      aps_1_phasor,      0,      0,      0,    0,      0,      0,      0,      0,      0],
                    [0,      0,      0,      1,      0,      0,    0,      0,      0,      0,      0,      0],
                    [0,      0,      0,      0,      1,      0,    0,      0,      0,      0,      0,      0],
                    [0,      0,      0,      0,      0,      aps_2_phasor,    0,      0,      0,      0,      0,      0],
                    [0,      0,      0,      0,      0,      0,    1,      0,      0,      0,      0,      0],
                    [0,      0,      0,      0,      0,      0,    0,      1,      0,      0,      0,      0],
                    [0,      0,      0,      0,      0,      0,    0,      0,      aps_3_phasor,  0,      0,      0],
                    [0,      0,      0,      0,      0,      0,    0,      0,      0,      1,      0,      0],
                    [0,      0,      0,      0,      0,      0,    0,      0,      0,      0,      1,      0],
                    [0,      0,      0,      0,      0,      0,    0,      0,      0,      0,      0,      1]])

        # tricoupler transfer matrix (all at once)
        T_tri = np.sqrt(1./3.) * np.array([[1,         phase_term_1, phase_term_1,     0,          0,          0,          0,          0,          0,          0,                   0,              0], 
                                        [phase_term_1, 1,          phase_term_1,     0,          0,          0,          0,          0,          0,          0,                      0,              0],
                                        [phase_term_1, phase_term_1, 1         ,     0,          0,          0,          0,          0,          0,          0,                      0,              0],
                                        [0,          0,          0         ,     1,          phase_term_2, phase_term_2, 0,          0,          0,          0,                      0,              0],
                                        [0,          0,          0         ,     phase_term_2, 1,          phase_term_2, 0,          0,          0,          0,                      0,              0],
                                        [0,          0,          0         ,     phase_term_2, phase_term_2, 1,          0,          0,          0,          0,                      0,              0],
                                        [0,          0,          0         ,     0,          0,          0,          1,          phase_term_3, phase_term_3, 0,                      0,              0],
                                        [0,          0,          0         ,     0,          0,          0,          phase_term_3, 1,          phase_term_3, 0,                      0,              0],
                                        [0,          0,          0         ,     0,          0,          0,          phase_term_3, phase_term_3, 1,          0,                      0,              0],
                                        [0,          0,          0         ,     0,          0,          0,          0,          0,          0,          np.sqrt(3.),         0,              0],
                                        [0,          0,          0         ,     0,          0,          0,          0,          0,          0,          0,                      np.sqrt(3.), 0],
                                        [0,          0,          0         ,     0,          0,          0,          0,          0,          0,          0,                      0,              np.sqrt(3.)]])


        phase_aps_list = []  # Initialize an empty list for phase_right values

        # loop over APS values (all three APSes are being dialed equally here)
        phase_aps_array = np.linspace(0, 2*np.pi, 100)
        flux_output_matrix = np.zeros((12,len(phase_aps_array)))  # Initialize an array
        i = 0 # initial index for flux output row
        for phase_aps_val in phase_aps_array:
                # achromatic phase shifters, now arranged as a matrix
                phase_shift_1 = phase_aps_val # induced by phase shifters for baseline 1 in waveguide; assumed achromatic; 120 deg = 2*pi/3
                phase_shift_2 = phase_aps_val 
                phase_shift_3 = phase_aps_val
                phasor_aps_1 = np.exp(1j * phase_shift_1) # achromatic phase shift term
                phasor_aps_2 = np.exp(1j * phase_shift_2)
                phasor_aps_3 = np.exp(1j * phase_shift_3)

                P_aps = np.array([[1,      0,      0,      0,      0,      0,    0,      0,      0,      0,      0,      0], 
                        [0,      1,      0,      0,      0,      0,    0,      0,      0,      0,      0,      0],
                        [0,      0,      phasor_aps_1,      0,      0,      0,    0,      0,      0,      0,      0,      0],
                        [0,      0,      0,      1,      0,      0,    0,      0,      0,      0,      0,      0],
                        [0,      0,      0,      0,      1,      0,    0,      0,      0,      0,      0,      0],
                        [0,      0,      0,      0,      0,      phasor_aps_2,    0,      0,      0,      0,      0,      0],
                        [0,      0,      0,      0,      0,      0,    1,      0,      0,      0,      0,      0],
                        [0,      0,      0,      0,      0,      0,    0,      1,      0,      0,      0,      0],
                        [0,      0,      0,      0,      0,      0,    0,      0,      phasor_aps_3,  0,      0,      0],
                        [0,      0,      0,      0,      0,      0,    0,      0,      0,      1,      0,      0],
                        [0,      0,      0,      0,      0,      0,    0,      0,      0,      0,      1,      0],
                        [0,      0,      0,      0,      0,      0,    0,      0,      0,      0,      0,      1]])



                flux_output = np.abs(np.dot(T_tri, 
                                        np.dot(P_aps,
                                                np.dot(M_interf,   
                                                        np.dot(M_phot,a_in)
                                                        )
                                                )
                                        )
                                )**2
                
                flux_output_matrix[:,i] = flux_output # append flux_output to the list
                i+=1 # increment i
                phase_aps_list.append(phase_aps_val)  # append phase to the list

                phase_aps_matrix = np.array(phase_aps_list)
                flux_output_matrix = np.array(flux_output_matrix)


        phase_aps_matrix_deg = phase_aps_matrix * np.pi/180.

        # plot for checking
        plot_file_name = 'test.png'
        plt.plot(phase_aps_matrix_deg, flux_output_matrix[0,:], label='I_B1A', linestyle=":")
        plt.plot(phase_aps_matrix_deg, flux_output_matrix[1,:], label='I_N1', linewidth=4)
        plt.plot(phase_aps_matrix_deg, flux_output_matrix[2,:], label='I_B1B', linestyle=":")
        plt.plot(phase_aps_matrix_deg, flux_output_matrix[3,:], label='I_B2A', linestyle=":")
        plt.plot(phase_aps_matrix_deg, flux_output_matrix[4,:], label='I_N2', linewidth=4)
        plt.plot(phase_aps_matrix_deg, flux_output_matrix[5,:], label='I_B2B', linestyle=":")
        plt.plot(phase_aps_matrix_deg, flux_output_matrix[6,:], label='I_B3A', linestyle=":")
        plt.plot(phase_aps_matrix_deg, flux_output_matrix[7,:], label='I_N3', linewidth=4)
        plt.plot(phase_aps_matrix_deg, flux_output_matrix[8,:], label='I_B3B', linestyle=":")
        plt.plot(phase_aps_matrix_deg, flux_output_matrix[9,:], label='P1', linestyle="--")
        plt.plot(phase_aps_matrix_deg, flux_output_matrix[10,:], label='P2', linestyle="--")
        plt.plot(phase_aps_matrix_deg, flux_output_matrix[11,:], label='P3', linestyle="--")
        plt.ylabel('Intensity')
        plt.xlabel('Achromatic phase delay')
        plt.legend()
        #plt.show()
        plt.savefig(plot_file_name)

        print('Wrote',plot_file_name)

        return