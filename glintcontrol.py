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


    def sim_chip():

        return 1