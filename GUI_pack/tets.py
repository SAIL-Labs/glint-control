import matplotlib.pyplot as plt
import numpy as np
import sys
sys.path.append('/Users/sbry5606/phd/phd-code/chip-sim')
# sys.path.append('/home/scexao/steph/control-code')

# from chip import Chip
from spectra import plot_spectra as spectra

figure = plt.figure()#figsize=(3.2, 2))

n_apertures = 3
n_phot = 3
n_tricoupler = 3
n_directional = 0
coeff_photo = np.array([1/3, 1/3, 1/3])
coeff_interf = np.array([1/2, 1/2, 1/2])

aperture = 1
opd = 0

x = np.zeros(3)
x[aperture] = opd

axs = spectra(aperture, x, n_apertures, n_phot, n_tricoupler, n_directional, coeff_photo, coeff_interf, figure)

plt.show()