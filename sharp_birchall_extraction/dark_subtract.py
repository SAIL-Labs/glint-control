#!/usr/bin/env python
# coding: utf-8

import numpy as np
from glob import glob
import os
from astropy.io import fits
import ipdb

stem = '/home/scexao/eckhart/spectral_extraction_test_20240927/data/'

file_list_data = glob(stem + 'raw/*.fits')
file_name_dark = stem + 'calibs/test_dark.fits'
dir_write = stem + 'dark_subted/'


# read in dark
with fits.open(file_name_dark) as hdul:
    dark = hdul[0].data

    # take median along cube
    dark = np.median(dark, axis=0)

ipdb.set_trace()
for file_name in file_list_data:
    # read in one FITS file data cube
    
    with fits.open(file_name) as hdul:
        
        data = hdul[0].data
        
        # subtract dark from each slice of the cube
        ipdb.set_trace()
        data = np.subtract(data,dark)

        abs_save_name = dir_write + os.path.basename(file_name)

        new_hdul = fits.HDUList([fits.PrimaryHDU(data)])

        new_hdul.writeto(abs_save_name, overwrite=True)
        print('Wrote',abs_save_name)