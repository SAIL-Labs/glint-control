# Reads in frames and splits them into sections, based on the divisions in y

import glob
import astropy.io.fits as fits
import matplotlib.pyplot as plt
import ipdb

# directory containing frames to split
dir_read = '/Users/bandari/Downloads/masked_frames/'

file_names = glob.glob(dir_read + '*.fits')

# at what y-values should frames be split? (include 0 and -1)
splits_in_y = [0,20,40,70,-1]

for file_num in range(0,len(file_names)):

    # Read in the first FITS file
    with fits.open(file_names[file_num]) as hdul:
        data = hdul[0].data
        header = hdul[0].header

        for split_num in range(len(splits_in_y)-1):

            data_string = 'data_' + str(split_num)
            
            data_section = data[splits_in_y[split_num]:splits_in_y[split_num+1]]
            print('------')
            print(split_num)
            print(split_num+1)

            plt.clf()
            plt.imshow(data_section)
            plt.show()

        # Save the split data to a new FITS file
        #split_file_name = f"{file_names[file_num][:-5]}_split_{i}.fits"
        #fits.writeto(split_file_name, split_data, split_header, overwrite=True)