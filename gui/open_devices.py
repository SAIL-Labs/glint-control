'''
Open the MEMs and mount.
'''

import sys
sys.path.append('/home/scexao/glint/control-code')
import apiMEMsControl 
import shmMEMsControl
import chipMountControl 
from pyMilk.interfacing.shm import SHM

def open_mems():
    # mems = apiMEMsControl.MEMS('32AW038#027')
    # try:    
    #     mems.openDM()
    #     print('DM opened successfully')
        
    # except Exception as e:
    #     print('DM not opened successfully')
    #     print(e)
    #     sys.exit(1)

    mems = shmMEMsControl.MEMS()

    # mems = None

    
    return mems

def open_mount():
    # Commented this out to ensure teh code runs without the mount so tehre aren't two instance of mount running
    mount = chipMountControl.Mount('/dev/serial/by-id/usb-SURUGA_SEIKI_SURUGA_SEIKI_DS102-if00-port0', 38400)
    try:
        mount.idn()
        print('Mount opened successfully')
    except Exception as e:
        print('Mount not opened successfully')
        print(e)
        sys.exit(1)

    # mount = None

    return mount

def open_cameras():
    
    try:
        apapane = SHM('apapane')
    except Exception as e:
        apapane = None
        print('Apapane not opened successfully:', e)
    
    try:
        palila = SHM('palila')
    except Exception as e:
        palila = None
        print('Palila not opened successfully:', e)
    
    try:
        glint_pupil = SHM('glintpg1')
    except Exception as e:
        glint_pupil = None
        print('GLINT pupil camera not opened successfully:', e)
    
    try:
        glint_focal =  SHM('glintpg2')
    except Exception as e:
        glint_focal = None
        print('GLINT focal camera not opened successfully:', e)
        
    cameras = (apapane, palila, glint_pupil, glint_focal)

    return cameras

def devices():
    mems = open_mems()
    mount = open_mount()
    cams = open_cameras()
    return mems, mount, cams


