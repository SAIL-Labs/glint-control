#!/usr/bin/env python
# coding: utf-8

import ipdb
import numpy as np
from glob import glob
import os
from astropy.io import fits

stem = '/home/scexao/eckhart/spectral_extraction_test_20240927/data/'

file_name = stem + 'individual_slices/test_01_slice_009991.fits'
    
with fits.open(file_name) as hdul:
    
    data = hdul[0].data

    badpix = np.zeros(np.shape(data))

    badpix = np.squeeze(badpix)

    new_hdul = fits.HDUList([fits.PrimaryHDU(badpix)])

    abs_save_name = stem + 'calibs/badpix.fits'
    new_hdul.writeto(abs_save_name, overwrite=True)
    print('Wrote',abs_save_name)