import numpy as np
import matplotlib.pyplot as plt

# Refs:
# - Martinod+ 2021 Applied Optics 60(19), Appendix A
# - Klinner-Teo, thesis

# transfer matrix of 
# 3 tricouplers, with photometric taps from each input

##################################
## START USER INPUTS

# parameters of incoming complex wavefronts, before any splitting [units radians]
# (note these are upstream of the achromatic phase shift; these phases are NOT from the APSes)
amp_I = 1
phase_I = 0
amp_II = 1
phase_II = 0
amp_III = 1
phase_III = 0

# phase shifts induced by APSes in waveguides; assumed achromatic; 120 deg = 2*pi/3
phase_shift_1 = 2.*np.pi/3.
phase_shift_2 = 2.*np.pi/3.
phase_shift_3 = 2.*np.pi/3.

# splitting coefficient of that going into photometric tap at each such split (values for waveguides 1 and 2 assumed the same)
## ## TO DO: allow for 3 different vals
alpha_val = 0.2
# splitting coefficients just before coupling stage (note that certain pairs have to sum to 1)
## ## TO DO: reduce to x, 1-x pairs
beta_val, gamma_val = 0.4, 0.6
delta_val, omega_val = 0.5, 0.5
eta_val, sigma_val = 0.3, 0.7

## END USER INPUTS
##################################

# input wavefonts
phasor_in_I = amp_I * np.exp(1j * phase_I)
phasor_in_II = amp_II * np.exp(1j * phase_II)
phasor_in_III = amp_III * np.exp(1j * phase_III)
a_in = np.array([phasor_in_I, phasor_in_II, phasor_in_III])

# phasors for APSes
phase_term_1 = np.exp(1j * phase_shift_1)
phase_term_2 = np.exp(1j * phase_shift_2)
phase_term_3 = np.exp(1j * phase_shift_3)

# transfer matrix of photometric splitting
M_phot = np.array([[1 - alpha_val,         0,               0], 
                   [0,                     1 - alpha_val,               0],
                   [0,                     0,              1 - alpha_val],
                   [alpha_val,             0,              0],
                   [0,             alpha_val,              0],
                   [0,                     0,              alpha_val]])

# transfer matrix of interferometric splitting
M_interf = np.array([[beta_val,      0,      0,      0,      0,      0], 
                   [0,      0,      0,      0,      0,      0], 
                   [0,      delta_val,      0,      0,      0,      0], 
                   [0,      omega_val,      0,      0,      0,      0], 
                   [0,      0,      0,      0,      0,      0], 
                   [0,      0,      eta_val,      0,      0,      0],
                   [gamma_val,      0,      0,      0,      0,      0],
                   [0,      0,      0,      0,      0,      0],
                   [0,      0,      sigma_val,      0,      0,      0],
                   [0,      0,      0,      1,      0,      0],
                   [0,      0,      0,      0,      1,      0],
                   [0,      0,      0,      0,      0,      1]])

# achromatic phase shifters, now arranged as a matrix
aps_1_phasor = np.exp(1j * phase_shift_1)
aps_2_phasor = np.exp(1j * phase_shift_2)
aps_3_phasor = np.exp(1j * phase_shift_3)

P_aps = np.array([[1,      0,      0,      0,      0,      0,    0,      0,      0,      0,      0,      0], 
             [0,      1,      0,      0,      0,      0,    0,      0,      0,      0,      0,      0],
             [0,      0,      aps_1_phasor,      0,      0,      0,    0,      0,      0,      0,      0,      0],
             [0,      0,      0,      1,      0,      0,    0,      0,      0,      0,      0,      0],
             [0,      0,      0,      0,      1,      0,    0,      0,      0,      0,      0,      0],
             [0,      0,      0,      0,      0,      aps_2_phasor,    0,      0,      0,      0,      0,      0],
             [0,      0,      0,      0,      0,      0,    1,      0,      0,      0,      0,      0],
             [0,      0,      0,      0,      0,      0,    0,      1,      0,      0,      0,      0],
             [0,      0,      0,      0,      0,      0,    0,      0,      aps_3_phasor,  0,      0,      0],
             [0,      0,      0,      0,      0,      0,    0,      0,      0,      1,      0,      0],
             [0,      0,      0,      0,      0,      0,    0,      0,      0,      0,      1,      0],
             [0,      0,      0,      0,      0,      0,    0,      0,      0,      0,      0,      1]])

# tricoupler transfer matrix (all at once)
T_tri = np.sqrt(1./3.) * np.array([[1,         phase_term_1, phase_term_1,     0,          0,          0,          0,          0,          0,          0,                   0,              0], 
                                   [phase_term_1, 1,          phase_term_1,     0,          0,          0,          0,          0,          0,          0,                      0,              0],
                                   [phase_term_1, phase_term_1, 1         ,     0,          0,          0,          0,          0,          0,          0,                      0,              0],
                                   [0,          0,          0         ,     1,          phase_term_2, phase_term_2, 0,          0,          0,          0,                      0,              0],
                                   [0,          0,          0         ,     phase_term_2, 1,          phase_term_2, 0,          0,          0,          0,                      0,              0],
                                   [0,          0,          0         ,     phase_term_2, phase_term_2, 1,          0,          0,          0,          0,                      0,              0],
                                   [0,          0,          0         ,     0,          0,          0,          1,          phase_term_3, phase_term_3, 0,                      0,              0],
                                   [0,          0,          0         ,     0,          0,          0,          phase_term_3, 1,          phase_term_3, 0,                      0,              0],
                                   [0,          0,          0         ,     0,          0,          0,          phase_term_3, phase_term_3, 1,          0,                      0,              0],
                                   [0,          0,          0         ,     0,          0,          0,          0,          0,          0,          np.sqrt(3.),         0,              0],
                                   [0,          0,          0         ,     0,          0,          0,          0,          0,          0,          0,                      np.sqrt(3.), 0],
                                   [0,          0,          0         ,     0,          0,          0,          0,          0,          0,          0,                      0,              np.sqrt(3.)]])


phase_aps_list = []  # Initialize an empty list for phase_right values

# loop over APS values (all three APSes are being dialed equally here)
phase_aps_array = np.linspace(0, 2*np.pi, 100)
flux_output_matrix = np.zeros((12,len(phase_aps_array)))  # Initialize an array
i = 0 # initial index for flux output row
for phase_aps_val in phase_aps_array:
        # achromatic phase shifters, now arranged as a matrix
        phase_shift_1 = phase_aps_val # induced by phase shifters for baseline 1 in waveguide; assumed achromatic; 120 deg = 2*pi/3
        phase_shift_2 = phase_aps_val 
        phase_shift_3 = phase_aps_val
        phasor_aps_1 = np.exp(1j * phase_shift_1) # achromatic phase shift term
        phasor_aps_2 = np.exp(1j * phase_shift_2)
        phasor_aps_3 = np.exp(1j * phase_shift_3)

        P_aps = np.array([[1,      0,      0,      0,      0,      0,    0,      0,      0,      0,      0,      0], 
                [0,      1,      0,      0,      0,      0,    0,      0,      0,      0,      0,      0],
                [0,      0,      phasor_aps_1,      0,      0,      0,    0,      0,      0,      0,      0,      0],
                [0,      0,      0,      1,      0,      0,    0,      0,      0,      0,      0,      0],
                [0,      0,      0,      0,      1,      0,    0,      0,      0,      0,      0,      0],
                [0,      0,      0,      0,      0,      phasor_aps_2,    0,      0,      0,      0,      0,      0],
                [0,      0,      0,      0,      0,      0,    1,      0,      0,      0,      0,      0],
                [0,      0,      0,      0,      0,      0,    0,      1,      0,      0,      0,      0],
                [0,      0,      0,      0,      0,      0,    0,      0,      phasor_aps_3,  0,      0,      0],
                [0,      0,      0,      0,      0,      0,    0,      0,      0,      1,      0,      0],
                [0,      0,      0,      0,      0,      0,    0,      0,      0,      0,      1,      0],
                [0,      0,      0,      0,      0,      0,    0,      0,      0,      0,      0,      1]])



        flux_output = np.abs(np.dot(T_tri, 
                                np.dot(P_aps,
                                        np.dot(M_interf,   
                                                np.dot(M_phot,a_in)
                                                )
                                        )
                                )
                        )**2
        
        flux_output_matrix[:,i] = flux_output # append flux_output to the list
        i+=1 # increment i
        phase_aps_list.append(phase_aps_val)  # append phase to the list

        phase_aps_matrix = np.array(phase_aps_list)
        flux_output_matrix = np.array(flux_output_matrix)


phase_aps_matrix_deg = phase_aps_matrix * np.pi/180.

# plot
plt.plot(phase_aps_matrix_deg, flux_output_matrix[0,:], label='I_B1A', linestyle=":")
plt.plot(phase_aps_matrix_deg, flux_output_matrix[1,:], label='I_N1', linewidth=4)
plt.plot(phase_aps_matrix_deg, flux_output_matrix[2,:], label='I_B1B', linestyle=":")
plt.plot(phase_aps_matrix_deg, flux_output_matrix[3,:], label='I_B2A', linestyle=":")
plt.plot(phase_aps_matrix_deg, flux_output_matrix[4,:], label='I_N2', linewidth=4)
plt.plot(phase_aps_matrix_deg, flux_output_matrix[5,:], label='I_B2B', linestyle=":")
plt.plot(phase_aps_matrix_deg, flux_output_matrix[6,:], label='I_B3A', linestyle=":")
plt.plot(phase_aps_matrix_deg, flux_output_matrix[7,:], label='I_N3', linewidth=4)
plt.plot(phase_aps_matrix_deg, flux_output_matrix[8,:], label='I_B3B', linestyle=":")
plt.plot(phase_aps_matrix_deg, flux_output_matrix[9,:], label='P1', linestyle="--")
plt.plot(phase_aps_matrix_deg, flux_output_matrix[10,:], label='P2', linestyle="--")
plt.plot(phase_aps_matrix_deg, flux_output_matrix[11,:], label='P3', linestyle="--")
plt.ylabel('Intensity')
plt.xlabel('Achromatic phase delay')
plt.legend()
#plt.show()
plt.savefig('test.png')