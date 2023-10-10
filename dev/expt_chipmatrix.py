import numpy as np
import matplotlib.pyplot as plt
plt.ion()

def make_chipmatrix():
    ### Define a complex transfer matrix representing the chip

    # Define input space
    input_wgs = np.array([1, 2, 3])
    input_segs = np.array([1, 2, 3]) # To contain actual MEMS seg numbers
    baselines = np.array([[1, 2], [2, 3], [1, 3]])

    # Define output space
    output_wgs = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
    output_wg_labels = ['P1', 'B1A', 'N1', 'B1B', 'P2', 'B2A', 'N2',
                        'B2B', 'P3', 'B3A', 'N3', 'B3B',]


    # Coefficient values
    p = np.sqrt(0.3) # Photometric tap fraction (amplitude)
    q = np.sqrt(1-p**2) # Non-photometric tap fraction (amplitude)
    s0 = q * np.sqrt(0.5) #* np.exp(1j * 0) # s0 - main split ratio (ampl), no phase offset
    sp = q * np.sqrt(0.5) * np.exp(1j * np.pi) # s+ - main split ratio (ampl), with pi delay (i.e. APS)
    t0 = np.sqrt(1/3) * np.exp(1j * 0) # t0 - tricoupler split ratio (ampl), no phase offset (i.e. null output)
    tm = np.sqrt(1/3) * np.exp(1j * 2*np.pi/3) # t- - tricoupler split ratio (ampl), +120 deg phase offset (i.e. bright output 1)
    tp = np.sqrt(1/3) * np.exp(1j * -2*np.pi/3) # t+ - tricoupler split ratio (ampl), -120deg phase offset (i.e. bright output 2)
    # tm = t0
    # tp = t0
    # tm = np.sqrt(1/3) * np.exp(1j * np.pi/5) # t- - tricoupler split ratio (ampl), +120 deg phase offset (i.e. bright output 1)
    # tp = np.sqrt(1/3) * np.exp(1j * -np.pi/5) # t+ - tricoupler split ratio (ampl), -120deg phase offset (i.e. bright output 2)



    # print([t0, tm, tp])

    # Pre-delays - the nominal phase delay applied by MEMS before injection
    pre_delays = np.array([np.pi, np.pi, 0])

    # Assemble transfer matrix
    chip_mat = np.array([
        [     p, sp*tm, sp*t0, sp*tp,     0,     0,     0,     0,     0, s0*tm, s0*t0, s0*tp],
        [     0, s0*tm, s0*t0, s0*tp,     p, sp*tm, sp*t0, sp*tp,     0,     0,     0,     0],
        [     0,     0,     0,     0,     0, s0*tm, s0*t0, s0*tp,     p, sp*tm, sp*t0, sp*tp]
    ])

    # input_ampls = np.array([ 0.        +0.j        ,  1.        +0.j        ,
    #    -0.12884449+0.99166481j])
    # print(input_ampls @ [sp * tm, sp * t0, sp * tp])
    # print(input_ampls @ [s0*tm, s0*t0, s0*tp])

    return chip_mat


def plot_chipoutput_fluxes(input_fields):
    ### Test matrix
    output_wgs = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
    output_wg_labels = ['P1', 'B1A', 'N1', 'B1B', 'P2', 'B2A', 'N2',
                        'B2B', 'P3', 'B3A', 'N3', 'B3B',]
    chip_mat = make_chipmatrix()
    # input_fields = np.array([1, 0, 0])

    # output_fields = input_fields @ chip_mat
    output_fields = chip_mat.T @ input_fields
    print(input_fields.shape)

    output_fluxes = np.abs(output_fields)**2

    plt.figure(1)
    plt.clf()
    plt.bar(output_wgs, output_fluxes)
    plt.xlabel('Output waveguide')
    plt.xticks(output_wgs, output_wg_labels)
    plt.ylabel('Output flux')



# plot_chipoutput_fluxes([1,0,0])

TCmat = np.sqrt(1/3) * np.array([ [1, np.exp(1j * 2*np.pi/3), np.exp(1j * 2*np.pi/3)],
                                  [np.exp(1j * 2*np.pi/3), 1, np.exp(1j * 2*np.pi/3)],
                                  [np.exp(1j * 2*np.pi/3), np.exp(1j * 2*np.pi/3), 1]
                                ])

# Test ramping phase
bl_ind = 0

for phi in np.arange(-np.pi, np.pi/2, 0.4):
    input_wgs = np.array([1, 2, 3])
    baselines = np.array([[1, 2], [2, 3], [1, 3]])
    input_ampls = np.zeros(input_wgs.shape, dtype='complex128')

    input_ampls1 = 1
    input_ampls2 = 1 * np.exp(1j * phi)
    ### TODO - fix baseline indexing
    inwg_inds = np.array([ np.where(input_wgs==baselines[bl_ind,0])[0][0],
                          np.where(input_wgs==baselines[bl_ind,1])[0][0] ])
    input_ampls[baselines[bl_ind, inwg_inds[0]]] = input_ampls1
    input_ampls[baselines[bl_ind, inwg_inds[1]]] = input_ampls2

    plot_chipoutput_fluxes(input_ampls)

    # output_fluxes = np.abs(TCmat @ np.array([input_ampls1, 0, input_ampls2]))**2
    # plt.figure(1)
    # plt.clf()
    # plt.bar([1,2,3], output_fluxes)
    # plt.xlabel('Output waveguide')
    # plt.ylabel('Output flux')

    plt.ylim([0,2])
    plt.title(phi)
    plt.pause(0.01)


# chip_mat = make_chipmatrix()
# output_fields = input_ampls @ chip_mat

# input_ampls @ [sp*tm, sp*t0, sp*tp]





