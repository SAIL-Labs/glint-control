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

stem = '/Users/bandari/Downloads/yoo-jung-smf/'

file_list = glob.glob(stem + '*.fits')

dir_write = stem + 'simple_sum/'
    
for file_name in file_list:

    with fits.open(file_name) as hdul:
        
        data = hdul[0].data

        spec_1d = np.sum(data[99:108,:], axis=0)

        # write plot
        plt.clf()
        plt.plot(spec_1d, color='r')
        file_write_name_plot = dir_write + os.path.basename(file_name).split('.')[0] + '.png'
        plt.savefig(file_write_name_plot)
        print('Wrote', file_write_name_plot)

        # write csv
        spec_1d_df = pd.DataFrame(spec_1d)
        file_write_name_csv = dir_write + os.path.basename(file_name).split('.')[0] + '.csv'
        spec_1d_df.to_csv(file_write_name_csv, index=False, header=False)
        print('Wrote',file_write_name_csv)