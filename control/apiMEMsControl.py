import sys
sys.path.append('/home/scexao/steph/bmc/setup_files') # All of these files are in /home/scexao/src/hardwaresecrets/drivers/bmc111

import bmc
import numpy as np

DM_Piston = bmc.DM_Piston
DM_XTilt = bmc.DM_XTilt
DM_YTilt = bmc.DM_YTilt

class MEMS():
    def __init__(self, serial) -> None:
        self.dm = bmc.BmcDm()
        self.serial = serial
    
    
    def openDM(self) -> None:
        err_code = self.dm.open_dm(self.serial)
        if err_code:
            raise Exception(self.dm.error_string(err_code))
    
    def closeDM(self) -> None:
        self.dm.close_dm()

    def num_actuators(self) -> int:
        return self.dm.num_actuators()

    def send_data(self, data:np.ndarray) -> None:
        '''
        Sends a full array of actuator vaues to the DM.
        '''
        err_code = self.dm.send_data(data.tolist())
        if err_code:
            raise Exception(self.dm.error_string(err_code))
    
    def set_actuator(self, actuator: 'int', data: 'double') -> "int":
        '''
        Set the value of a single actuator.
        '''
        return self.dm.poke(actuator, data)
    
    def set_segment(self, segment: 'int', piston: 'double', xTilt: 'double', yTilt: 'double') -> "int":
        '''
        Set the PTT values of a segment.
        '''
        err_code =  self.dm.set_segment(segment, piston, xTilt, yTilt, True, True)

        if err_code == bmc.ERR_OUT_OF_LUT_RANGE:
            err_string = "Out of range! [%d, %d, %d]\n".format(piston, xTilt, yTilt)
            print(err_string)
            return err_code
        else:
            raise Exception(self.dm.error_string(err_code))

    
    def get_actuator_data(self) -> np.ndarray:
        return np.array(self.dm.get_actuator_data())
    
    def get_segment_range(self, segment: 'int', axis: 'DMSegmentAxis', piston: 'double', xTilt: 'double', yTilt: 'double', applyOffsets: 'bool') -> "int":
        return self.dm.get_segment_range(segment, axis, piston, xTilt, yTilt, applyOffsets)
    
    def flatten(self) -> None:
        flat = np.loadtxt('32AW038_1500nm.txt', dtype=float)
        self.send_data(flat)
    
    


# if __name__ == "__main__":
#     mems = MEMS('32AW038#027')
#     mems.openDM()
#     print("Number of actuators:", mems.num_actuators())
#     mems.closeDM()
#     print('DM opened and closed successfully')

    
