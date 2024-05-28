"""
The main class to handle controlling the GLINT instrument.
Eventually this will be wrapped in a GUI!
"""

import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from scipy.optimize import curve_fit

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
        # Later these could become their own objects
        self.current_camera_frame = None # Shape [width, height]
        self.stored_camera_frames = None # Shape [1000, width, height]. These are taken from the camera.
        self.current_flux_vectors = None # Shape [output_chans, wavelengths]
        self.stored_flux_vectors = None # Shape [1000, width]
        self.darkframe = None # The current darkframe to subtract before extracting fluxes
        # self.darkframe_vector = None # 10 lots of darkframes




    def get_latest_camera_frame(self, subtract_dark=True): #DONE
        ### STUB
        # Get the latest camera frame, subtract self.darkframe is requested, and store in
        # self.current_camera_frame.

        if subtract_dark:
            self.current_camera_frame = self.current_camera_frame - self.darkframe

        return self.current_camera_frame



    def get_darkframe(self, nframes=1, save_to_file=True, datapath=None, filepref=None): #DONE
        ### STUB
        # Set the latest nframes frames from the camera, average them, and set as self.darkframe.
        # Save the darkframe to a file if requested, to specified datapath and/or file prefix
        # if provided (see self.save_test_data() for more info).

        if datapath == None:
            datapath = self.datapath

        # Retrieve the last nframes frames from the stored camera array variable
        idx = len(self.stored_camera_frames) - nframes
        frames = self.stored_camera_frames[idx:]

        # Average over them
        avg_frames = np.mean(frames, axis = 0)
        self.darkframe = avg_frames

        if save_to_file:
            self.save_test_data(nframes, datapath, filepref)

        return self.darkframe

    def extract_flux(self, data, min_h, max_h, min_w = 0, max_w = 320): #DONE 
        cropped_image = [row[min_w:max_w + 1] for row in data[min_h:max_h + 1]]
        flux_vector = np.sum(cropped_image, axis=0)

        return flux_vector
    

    def get_latest_fluxes(self): # DONE
        ### STUB
        # Extract the flux vectors from self.current_camera_frame
        n_outputs = self.output_wgs.shape[0]
        n_wls = self.wl_channels.shape[0]

        self.current_flux_vectors = np.zeros((n_outputs, n_wls))

        data = self.current_camera_frame

        spec1_min_h = 100
        spec1_max_h = 107
        spec1 = self.extract_flux(data, spec1_min_h, spec1_max_h)

        spec2_min_h = 154
        spec2_max_h = 163
        spec2 = self.extract_flux(data, spec2_min_h, spec2_max_h)

        spec3_min_h = 174
        spec3_max_h = 182
        spec3 = self.extract_flux(data, spec3_min_h, spec3_max_h)

        self.current_flux_vectors = [spec1, spec2, spec3]

        return self.current_flux_vectors


    def save_test_data(self, nframes=1, datapath=None, filepref=None, save_raw_ims=False):
        ### STUB
        # Do a _slow_ save of nframes of extracted fluxes, and the raw camera frames if requested.
        # This is not realtime, so will miss many frames, so is just for testing and diagnostics.
        # npz format is probably best for now

        if datapath is None:
            datapath = self.datapath

        if filepref is None:
            dt = str(datetime.now())
            date = dt.split()[0]
            time = dt.split()[1]
            filepref = "{}_{}".format(date, time)

        # Retrieve the last nframes frames from the stored camera array variable
        idx = len(self.stored_camera_frames) - nframes # This should be the same for the stored fluxes
        frames = self.stored_camera_frames[idx:]
        fluxes = self.stored_flux_vectors[idx:]

        np.savez(datapath+filepref+'_fluxvec.npz', fluxvec = fluxes)

        if save_raw_ims:
            np.savez(datapath+filepref+'_cam.npz', camframe = frames) # Do fits file instead



    def set_MEMS_posns(self, input_wgs, cmd_posns):
        ### STUB
        # Sets the segment(s) corresponding to input_wg(s) to the given tip, tilt & piston values
        # cmd_posns is an nx3 array of form  [[tip, tilt, piston]], where n=len(input_wgs).
        # Then update self.mems_seg_tts and self.mems_seg_pists with the new values.
        # If an element in cmd_posns is None, leave the corresponding tip/tilt/piston position unchanged
        
        # I am assuming that input_wgs is self.input_wgs

        cmd_posns = np.array(cmd_posns) #  Need it to be numpy array otherwise indexing trick won't work
        old_tt = np.array(self.mems_seg_tts)
        old_pists = np.array(self.mems_seg_pists)
        
        temp_tt = cmd_posns[:,(0,1)]  #  Indexing trick that lets us select portion of 2D array
        temp_pists = cmd_posns[:,2]
            
        new_tt = np.where(temp_tt == None, old_tt, temp_tt)        
        new_pists = np.where(temp_pists == None, old_pists, temp_pists)

        self.mems_seg_tts = new_tt
        self.mems_seg_pists = new_pists
    
    



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
        

        # 1) Link input_wgs to a corresponding baseline
        #       can do this by first finding the index corresponsing to self.input_wgs and then using that index in further arrays
        # 2) Get the segment to be pistoned
        # 3) Scan the segment - for now just use a predefined x 
        # 4) Use the mean flux output as your y - more accurate rectangle size, easier it is to find optimum. 
        # 5) Find the fitted parameters
        # 6) Use the position corresponding to a minima because this is a null

        # x: piston position
        # y: mean flux output


        scan_step = 1000
        pretend_scan = np.linspace(-3,3,1000)
        y = 2*np.sin(np.pi*x+np.pi)+4

        null_model = lambda x, amp, freq, phase, offset: amp * np.sin(freq*x + phase) + offset

        init_guess = [2, 2, 0, 2]
        popt = curve_fit(null_model, self.real_piston, self.scanned_valued, p0=init_guess)[0]

        x = np.arange(-3, 3, scan_step/100)
        fit = null_model(x, *popt)
        best_null_pos = x[np.argmin(fit)]


path = '/Users/stephanie/PycharmProjects/GLINT/GLINT-control'
glintcontrol = glintcontrol(path)







