#!/usr/bin/env python
# coding: utf-8

import numpy as np
from glob import glob
import os
import ipdb
from astropy.io import fits

stem_read = '/import/morgana1/snert/GLINTData/data202409/20240918/apapane/'
stem_write = '/import/morgana1/snert/GLINTData/data202409/eckhart_reductions/darks/'

file_list_data = glob(stem_read + 'apapane_07:26*.fits')
file_name_dark_write = stem_write + 'dark_start_apapane_07:25:19.922087353.fits'

# Initialize an empty list to store the 2D frames
frames = []

# read in dark frames
for file_name in file_list_data:
    # read in one FITS file data cube
    print('Reading in',file_name)
    with fits.open(file_name) as hdul:
        dark_this = hdul[0].data
        
        # Append the 2D frame to the list
        frames.append(dark_this)

# Convert the list of frames into a 3D NumPy array
ipdb.set_trace()
cube = np.array(frames)

# Take the median along the third axis
median_frame = np.median(cube, axis=0)

# Save the median frame to a new FITS file
median_hdul = fits.HDUList([fits.PrimaryHDU(median_frame)])
median_hdul.writeto(file_name_dark_write, overwrite=True)
print('Wrote', file_name_dark_write)