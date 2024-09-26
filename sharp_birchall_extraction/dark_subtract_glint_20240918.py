#!/usr/bin/env python
# coding: utf-8

import numpy as np
from glob import glob
import os
from astropy.io import fits

stem_read = '/import/morgana1/snert/GLINTData/data202409/20240918/apapane/'
stem_write = '/import/morgana1/snert/GLINTData/data202409/eckhart_reductions/dark_subted/20240918/apapane/'


file_list_data_1 = glob(stem_read + 'apapane_06:5*.fits')
file_list_data_2 = glob(stem_read + 'apapane_07:[0-2]*.fits')
file_list_data = file_list_data_1 + file_list_data_2

file_name_dark = '/import/morgana1/snert/GLINTData/data202409/eckhart_reductions/darks/dark_start_apapane_07:25:19.922087353.fits'

# read in dark
with fits.open(file_name_dark) as hdul:
    dark = hdul[0].data

for file_name in file_list_data:
    # read in one FITS file data cube
    
    with fits.open(file_name) as hdul:
        
        data = hdul[0].data

        # take median of cube
        data = np.median(data, axis=0)
        
        data = np.subtract(data,dark)

        abs_save_name = stem_write + os.path.basename(file_name)

        new_hdul = fits.HDUList([fits.PrimaryHDU(data)])

        new_hdul.writeto(abs_save_name, overwrite=True)
        print('Wrote',abs_save_name)