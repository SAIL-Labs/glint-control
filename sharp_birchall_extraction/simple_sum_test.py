#!/usr/bin/env python
# coding: utf-8

# makes a simple sum in a subarray of FITS files and plots it, to compare with more
# fancy extractions

import numpy as np
import ipdb
import glob
import os
import pandas as pd
from astropy.io import fits
import matplotlib.pyplot as plt

#stem = '/Users/bandari/Downloads/yoo-jung-smf/'
stem = '/Users/bandari/Documents/git.repos/GLINT_reduction_v3/data/sample_data/'

#file_list = glob.glob(stem + '*.fits')
file_list = glob.glob(stem + 'test_02_slice_008500.fits')

dir_write = stem + 'junk/'
    
for file_name in file_list:

    with fits.open(file_name) as hdul:
        
        data = hdul[0].data

        spec_1d_00 = np.sum(data[236:241,:], axis=0)
        spec_1d_01 = np.sum(data[217:223,:], axis=0)
        spec_1d_02 = np.sum(data[198:204,:], axis=0)
        spec_1d_03 = np.sum(data[180:185,:], axis=0)
        spec_1d_04 = np.sum(data[162:167,:], axis=0)
        spec_1d_05 = np.sum(data[142:147,:], axis=0)
        spec_1d_06 = np.sum(data[124:128,:], axis=0)
        spec_1d_07 = np.sum(data[105:109,:], axis=0)
        spec_1d_08 = np.sum(data[85:90,:], axis=0)
        spec_1d_09 = np.sum(data[48:52,:], axis=0)
        spec_1d_10 = np.sum(data[30:33,:], axis=0)
        spec_1d_11 = np.sum(data[9:14,:], axis=0)

        # write plot
        plt.clf()
        offset = 50000
        plt.plot(spec_1d_00 + 0*offset)
        plt.plot(spec_1d_01 + 1*offset)
        plt.plot(spec_1d_02 + 2*offset)
        plt.plot(spec_1d_03 + 3*offset)
        plt.plot(spec_1d_04 + 4*offset)
        plt.plot(spec_1d_05 + 5*offset)
        plt.plot(spec_1d_06 + 6*offset)
        plt.plot(spec_1d_07 + 7*offset)
        plt.plot(spec_1d_08 + 8*offset)
        plt.plot(spec_1d_09 + 9*offset)
        plt.plot(spec_1d_10 + 10*offset)
        plt.plot(spec_1d_11 + 11*offset)
        file_write_name_plot = dir_write + os.path.basename(file_name).split('.')[0] + '.png'
        plt.savefig(file_write_name_plot)
        print('Wrote', file_write_name_plot)

        # write csv
        spec_1d_df = pd.DataFrame(spec_1d)
        file_write_name_csv = dir_write + os.path.basename(file_name).split('.')[0] + '.csv'
        spec_1d_df.to_csv(file_write_name_csv, index=False, header=False)
        print('Wrote',file_write_name_csv)