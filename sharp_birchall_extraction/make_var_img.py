#!/usr/bin/env python
# coding: utf-8

import numpy as np
import ipdb
from glob import glob
import os
from astropy.io import fits

stem = '/home/scexao/eckhart/spectral_extraction_test_20240927/data/'

file_name = stem + 'dark_subt/test_02.fits'

dir_write = stem + 'calibs/'
    
with fits.open(file_name) as hdul:
    
    data = hdul[0].data

    # if this is a cube, take median along the cube
    data = np.median(data, axis=0)
    
    # find variance
    data = np.sqrt(data)

    # replace nans with median
    median_value = np.nanmedian(data)
    data = np.where(np.isnan(data), median_value, data)

    #data = np.rot90(np.squeeze(data))
    data = np.squeeze(data)

    new_hdul = fits.HDUList([fits.PrimaryHDU(data)])

    abs_save_name = dir_write + 'variance.fits'
    new_hdul.writeto(abs_save_name, overwrite=True)
    print('Wrote',abs_save_name)