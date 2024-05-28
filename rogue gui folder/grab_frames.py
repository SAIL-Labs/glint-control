import numpy as np
from pyMilk.interfacing.shm import SHM

pupil = SHM('glintpg1')
image = SHM('glintpg2')

p = pupil.get_data() # 1 frame
i = image.get_data() # 1 frame

np.savez('pupil_image_2024-04-04.npz', pupil=p, image=i)

