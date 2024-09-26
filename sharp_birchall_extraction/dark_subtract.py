#!/usr/bin/env python
# coding: utf-8

import numpy as np
from glob import glob
import os
from astropy.io import fits

stem = '/Users/bandari/Documents/git.repos/glint-control/sharp_birchall_extraction/yoo_jung_data_20240818/'

file_list_data = glob(stem + 'altair_raw/*.fits')
file_name_dark = stem + 'calibs/dark_apapane_11:47:01.304614609_trunc.fits'

# read in dark
with fits.open(file_name_dark) as hdul:
    dark = hdul[0].data

for file_name in file_list_data:
    # read in one FITS file data cube
    
    with fits.open(file_name) as hdul:
        
        data = hdul[0].data
        
        data = np.subtract(data,dark)

        abs_save_name = stem + 'altair_dark_subted/' + os.path.basename(file_name)

        new_hdul = fits.HDUList([fits.PrimaryHDU(data)])

        new_hdul.writeto(abs_save_name, overwrite=True)
        print('Wrote',abs_save_name)