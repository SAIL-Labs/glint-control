import sys
sys.path.append('/home/scexao/steph/control-code')

import apiMEMsControl 
import chipMountControl 

from control_buttons_ui import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt

DM_Piston = apiMEMsControl.DM_Piston
DM_XTilt = apiMEMsControl.DM_XTilt
DM_YTilt = apiMEMsControl.DM_YTilt

def preprocessing(gui):
    gui.list_segments.setVisible(False)


def triggers(gui):

    '''
    Test we have connection with MEMs and mount
    '''
    gui.pushButton_numActuators.clicked.connect(
        lambda: numActuators(gui, mems))
    
    gui.pushButton_setSpeed.clicked.connect(
        lambda: setSpeed(gui, mount))

    gui.pushButton_getSpeed.clicked.connect(
        lambda: getSpeed(gui, mount))
    
    ### Segment list ###
    # Connect the line edit's focus events to clear and restore the default text
    gui.text_segments.focusInEvent = lambda event: gui.text_segments.setText('')
    gui.text_segments.focusOutEvent = lambda event: get_segments(gui.text_segments.text(), gui.text_segments)

    # gui.text_segments.textChanged.connect(
    #     lambda text, le=gui.text_segments: get_segments(text, le))

    # gui.pushButton_numActuators.clicked.connect(
    #     lambda: print('hi'))
    
    # gui.pushButton_save.clicked.connect(gui.save)

    # ### MEMs control buttons ###
    # gui.pushButton_flattenMEMs.clicked.connect(flatten)


    # ### Manual control buttons ###
    # gui.pushButton_x_up.clicked.connect(
    #     lambda: x_up(gui, mount))
    # gui.pushButton_x_down.clicked.connect(
    #     lambda: x_down(gui, mount))
    # gui.pushButton_y_up.clicked.connect(
    #     lambda: y_up(gui, mount))
    # gui.pushButton_y_down.clicked.connect(
    #     lambda: y_down(gui, mount))
    # gui.pushButton_z_up.clicked.connect(
    #     lambda: z_up(gui, mount))
    # gui.pushButton_z_down.clicked.connect(
    #     lambda: z_down(gui, mount))
    # gui.pushButton_yaw_up.clicked.connect(
    #     lambda: yaw_up(gui, mount))
    # gui.pushButton_yaw_down.clicked.connect(
    #     lambda: yaw_down(gui, mount))
    # gui.pushButton_roll_up.clicked.connect(
    #     lambda: roll_up(gui, mount))
    # gui.pushButton_roll_down.clicked.connect(
    #     lambda: roll_down(gui, mount))
    # gui.pushButton_pitch_up.clicked.connect(
    #     lambda: pitch_up(gui, mount))
    # gui.pushButton_pitch_down.clicked.connect(  
    #     lambda: pitch_down(gui, mount))
    
    
    # gui. pushButton_piston_up.clicked.connect(
    #     lambda: pist_up(gui, mems))
    # gui.pushButton_piston_down.clicked.connect(
    #     lambda: pist_down(gui,  mems))
    # gui.pushButton_tip_up.clicked.connect(
    #     lambda: tip_up(gui, mems))
    # gui.pushButton_tip_down.clicked.connect(
    #     lambda: tip_down(gui, mems))
    # gui.pushButton_tilt_up.clicked.connect(
    #     lambda: tilt_up(gui, mems))
    # gui.pushButton_tilt_down.clicked.connect(
    #     lambda: tilt_down(gui, mems))

    

   
    
    # # ### Live cam checkbox ###
    # # gui.checkBox_livecam.stateChanged.connect(
    # #     lambda state, gui=gui: toggleLiveCam(gui, state))



    # ### Manual control checkboxes ###
    # gui.checkBox_manualMEMs.stateChanged.connect(
    #     lambda state: toggleMEMsEditable(gui, state))
    # gui.checkBox_manualMount.stateChanged.connect(
    #     lambda state: toggleMountEditable(gui, state))

    
    
    ### Set step sizes ###
    # gui.text_pistStepSize.textChanged.connect(
    #     lambda text, le=gui.text_pistStepSize: on_text_changed(text, le))
    # gui.text_ttStepSize.textChanged.connect(
    #     lambda text, le=gui.text_ttStepSize: on_text_changed(text, le))
    # gui.text_mountStepSize_urad.textChanged.connect(
    #     lambda text, le=gui.text_mountStepSize_urad: on_text_changed(text, le))
    # gui.text_mountStepSize_um.textChanged.connect(
    #     lambda text, le=gui.text_mountStepSize_um: on_text_changed(text, le))

    # gui.table_mountPos_rpy.itemChanged.connect(on_item_changed)
    # gui.table_mountPos_xyz.itemChanged.connect(on_item_changed)
    # gui.tab_memsPosition.itemChanged.connect(on_item_changed)


    '''
    Archived triggers
    '''
    # ### Toggle list widget ###
    # gui.toggleButton_segments.clicked.connect(
    #     lambda: toggleList(gui))

def numActuators(gui, mems):
    num_actuators = mems.num_actuators()
    print(num_actuators)
    gui.label_numActuators.setText(str(num_actuators))

def setSpeed(gui, mount):
    speed = int(gui.text_setSpeed.text())
    axis = 1
    mount.set_speed(axis, speed)

def getSpeed(gui, mount):
    axis = 1
    speed = mount.get_speed(axis)
    gui.label_getSpeed.setText(str(speed))

def flatten(gui, mems):
    mems.flatten()

    

def toggleList(gui):
    # Toggle the visibility of the list widget
    gui.list_segments.setVisible(not gui.list_segments.isVisible())

    # gui.list_segments.raise_()

def setTableEditable(table, editable):
    if editable:
        table.setEditTriggers(QtWidgets.QTableWidget.AllEditTriggers)
    else:
        table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
     
def toggleMEMsEditable(gui, state):
    '''
    This could be generalised but my brain hurts
    '''
    if state == 2:  # 2 corresponds to checked state
        gui.widget_manualMEMs_inner.setEnabled(True)
        gui.tab_memsPosition.setEditTriggers(QtWidgets.QTableWidget.AllEditTriggers)
    else:
        gui.widget_manualMEMs_inner.setEnabled(False)
        gui.tab_memsPosition.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

def toggleMountEditable(gui, state):
    if state == 2:  # 2 corresponds to checked state
        gui.widget_manualMount_inner.setEnabled(True)
        gui.table_mountPos_rpy.setEditTriggers(QtWidgets.QTableWidget.AllEditTriggers)
        gui.table_mountPos_xyz.setEditTriggers(QtWidgets.QTableWidget.AllEditTriggers)
    else:
        gui.widget_manualMount_inner.setEnabled(False)
        gui.table_mountPos_rpy.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        gui.table_mountPos_xyz.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)


def toggleLiveCam(gui, state):
    if state == 2:  # 2 corresponds to checked state
        gui.widget_selectFrame.setEnabled(False)
    else:
        gui.widget_selectFrame.setEnabled(True)
                                            
def on_text_changed(text, variable):
    try:
        value = float(text)
    except ValueError:
        variable.setText(None)
        print("Input value is not a float.")

def on_item_changed(item):
    try:
        float_value = float(item.text())
        # If the value is a valid float, allow the change
        item.setText("{:.3f}".format(float_value))  # Convert to 3 decimal places if it's a float
    except ValueError:
        # If the entered value is not a float, prevent the change
        item.setText("0.000")

def check_stepSize(stepsize):
    step = stepsize.text()

    if step is None:
        print("No step size given.")
        return None

    try:
        step = float(step)
        return step
    except ValueError:
        print("Step value is not a float.")
        return None

def get_checked_states(gui):
    # Get the checked state of each item in the QListWidget
    checked_states = []

    for i in range(gui.list_segments.count()):
        item = gui.list_segments.item(i)
        if item.checkState() == Qt.Checked:
            checked_states.append(int(item.text()))

    return checked_states

def get_segments(text, le):

    default = "E.g. [0, 4, 8]"

    if not text:
        le.setText(default)
        

    try:
        # Check if the string is in the format of an array
        segments = [int(s) for s in text.split(',')]
        print(segments)
        
    except ValueError:
        le.setText(default)
        print("Invalid format. Please enter numbers separated by commas.")
        

#

def pist_up(gui, mems):
    checked_items = get_checked_states(gui)
    stepsize = check_stepSize(gui.text_pistStepSize)
    if stepsize is not None:
        row = [r - 1 for r in checked_items]
        col = 0
        table = gui.tab_memsPosition

        for r in row:
            segment = r
            pist = float(table.item(r, col).text())
            tip = float(table.item(r, col + 1).text())
            tilt = float(table.item(r, col + 2).text())
            newpist = pist + stepsize

            mems.set_segment(segment, DM_Piston, newpist, tip, tilt, True)
            update_cell(table, r, col, newpist)

'''
Pseudocode:
Get the segment(s)
Get the current piston position
Add the step size to the current position
Set the new position
'''
def pist_down(gui, mems):
    checked_items = get_checked_states(gui)
    stepsize = check_stepSize(gui.text_pistStepSize)
    if stepsize is not None:
        row = [r - 1 for r in checked_items]
        col = 0
        table = gui.tab_memsPosition

        for r in row:
            segment = r
            pist = float(table.item(r, col).text())
            tip = float(table.item(r, col + 1).text())
            tilt = float(table.item(r, col + 2).text())
            newpist = pist - stepsize

            mems.set_segment(segment, DM_Piston, newpist, tip, tilt, True)
            update_cell(table, r, col, newpist)

def tip_up(gui, mems):

    checked_items = get_checked_states(gui)
    stepsize = check_stepSize(gui.text_pistStepSize)
    if stepsize is not None:
        row = [r - 1 for r in checked_items]
        col = 1
        table = gui.tab_memsPosition

        for r in row:
            segment = r
            pist = float(table.item(r, col - 1).text())
            tip = float(table.item(r, col).text())
            tilt = float(table.item(r, col + 1).text())
            newtip = tip + stepsize

            mems.set_segment(segment, DM_XTilt, pist, newtip, tilt, True)
            update_cell(table, r, col, newtip)

def tip_down(gui, mems):
    
    checked_items = get_checked_states(gui)
    stepsize = check_stepSize(gui.text_pistStepSize)
    if stepsize is not None:
        row = [r - 1 for r in checked_items]
        col = 1
        table = gui.tab_memsPosition

        for r in row:
            segment = r
            pist = float(table.item(r, col - 1).text())
            tip = float(table.item(r, col).text())
            tilt = float(table.item(r, col + 1).text())
            newtip = tip - stepsize

            mems.set_segment(segment, DM_XTilt, pist, newtip, tilt, True)
            update_cell(table, r, col, newtip)

def tilt_up(gui, mems):
    
    checked_items = get_checked_states(gui)
    stepsize = check_stepSize(gui.text_pistStepSize)
    if stepsize is not None:
        row = [r - 1 for r in checked_items]
        col = 2
        table = gui.tab_memsPosition

        for r in row:
            segment = r
            pist = float(table.item(r, col - 2).text())
            tip = float(table.item(r, col - 1).text())
            tilt = float(table.item(r, col).text())
            newtilt = tilt + stepsize

            mems.set_segment(segment, DM_YTilt, pist, tip, newtilt, True)
            update_cell(table, r, col, newtilt)


def tilt_down(gui, mems):

    checked_items = get_checked_states(gui)
    stepsize = check_stepSize(gui.text_pistStepSize)
    if stepsize is not None:
        row = [r - 1 for r in checked_items]
        col = 2
        table = gui.tab_memsPosition

        for r in row:
            segment = r
            pist = float(table.item(r, col - 2).text())
            tip = float(table.item(r, col - 1).text())
            tilt = float(table.item(r, col).text())
            newtilt = tilt - stepsize

            mems.set_segment(segment, DM_YTilt, pist, tip, newtilt, True)

            update_cell(table, r, col, newtilt)



def x_up(gui, mount):
    stepsize = check_stepSize(gui.text_mountStepSize_um)
    if stepsize is not None:
        table = gui.table_mountPos_xyz
        row = [0]
        col = 0
        axis = 4

        pos = mount.get_pos(axis)
        newpos = pos + stepsize
        mount.set_pos(axis, newpos)
        
        updated_pos = mount.get_pos(axis)
        update_cell(table, row, col, updated_pos)

        '''
        Pseudocode:
        Get the current mount position
        Add the step size to the current position
        Set the new position
        '''
    

def x_down(gui, mount):
    stepsize = check_stepSize(gui.text_mountStepSize_um)
    if stepsize is not None:
        table = gui.table_mountPos_xyz
        row = [0]
        col = 0
        axis = 4

        pos = mount.get_pos(axis)
        newpos = pos - stepsize
        mount.set_pos(axis, newpos)
        
        updated_pos = mount.get_pos(axis)
        update_cell(table, row, col, updated_pos)


def y_up(gui, mount):

    stepsize = check_stepSize(gui.text_mountStepSize_um)
    if stepsize is not None:
        table = gui.table_mountPos_xyz
        row = [0]
        col = 1
        axis = 6

        pos = mount.get_pos(axis)
        newpos = pos + stepsize
        mount.set_pos(axis, newpos)
        
        updated_pos = mount.get_pos(axis)
        update_cell(table, row, col, updated_pos)

def y_down(gui, mount):
    
    stepsize = check_stepSize(gui.text_mountStepSize_um)
    if stepsize is not None:
        table = gui.table_mountPos_xyz
        row = [0]
        col = 1
        axis = 6

        pos = mount.get_pos(axis)
        newpos = pos - stepsize
        mount.set_pos(axis, newpos)
        
        updated_pos = mount.get_pos(axis)
        update_cell(table, row, col, updated_pos)

def z_up(gui, mount):
    
    stepsize = check_stepSize(gui.text_mountStepSize_um)
    if stepsize is not None:
        table = gui.table_mountPos_xyz
        row = [0]
        col = 2
        axis = 5

        pos = mount.get_pos(axis)
        newpos = pos + stepsize
        mount.set_pos(axis, newpos)
        
        updated_pos = mount.get_pos(axis)
        update_cell(table, row, col, updated_pos)

def z_down(gui, mount):
    
    stepsize = check_stepSize(gui.text_mountStepSize_um)
    if stepsize is not None:
        table = gui.table_mountPos_xyz
        row = [0]
        col = 2
        axis = 5

        pos = mount.get_pos(axis)
        newpos = pos - stepsize
        mount.set_pos(axis, newpos)
        
        updated_pos = mount.get_pos(axis)
        update_cell(table, row, col, updated_pos)


def roll_up(gui, mount):
    
    stepsize = check_stepSize(gui.text_mountStepSize_urad)
    if stepsize is not None:
        table = gui.table_mountPos_rpy
        row = [0]
        col = 0
        axis = 2

        pos = mount.get_pos(axis)
        newpos = pos + stepsize
        mount.set_pos(axis, newpos)
        
        updated_pos = mount.get_pos(axis)
        update_cell(table, row, col, updated_pos)


def roll_down(gui, mount):
    
    stepsize = check_stepSize(gui.text_mountStepSize_urad)
    if stepsize is not None:
        table = gui.table_mountPos_rpy
        row = [0]
        col = 0
        axis = 2

        pos = mount.get_pos(axis)
        newpos = pos - stepsize
        mount.set_pos(axis, newpos)
        
        updated_pos = mount.get_pos(axis)
        update_cell(table, row, col, updated_pos)


def pitch_up(gui, mount):
    
    stepsize = check_stepSize(gui.text_mountStepSize_urad)
    if stepsize is not None:
        table = gui.table_mountPos_rpy
        row = [0]
        col = 1
        axis = 1

        pos = mount.get_pos(axis)
        newpos = pos + stepsize
        mount.set_pos(axis, newpos)
        
        updated_pos = mount.get_pos(axis)
        update_cell(table, row, col, updated_pos)


def pitch_down(gui, mount):
    
    stepsize = check_stepSize(gui.text_mountStepSize_urad)
    if stepsize is not None:
        table = gui.table_mountPos_rpy
        row = [0]
        col = 1
        axis = 1

        pos = mount.get_pos(axis)
        newpos = pos - stepsize
        mount.set_pos(axis, newpos)
        
        updated_pos = mount.get_pos(axis)
        update_cell(table, row, col, updated_pos)


def yaw_up(gui, mount):
    
    stepsize = check_stepSize(gui.text_mountStepSize_urad)
    if stepsize is not None:
        table = gui.table_mountPos_rpy
        row = [0]
        col = 2
        axis = 3

        pos = mount.get_pos(axis)
        newpos = pos + stepsize
        mount.set_pos(axis, newpos)
        
        updated_pos = mount.get_pos(axis)
        update_cell(table, row, col, updated_pos)


def yaw_down(gui, mount):

    stepsize = check_stepSize(gui.text_mountStepSize_urad)
    if stepsize is not None:
        table = gui.table_mountPos_rpy
        row = [0]
        col = 2
        axis = 3

        pos = mount.get_pos(axis)
        newpos = pos - stepsize
        mount.set_pos(axis, newpos)

        # should update cell by calling getpos again
        updatedpos = mount.get_pos(axis)
        update_cell(table, row, col, updatedpos)


def update_cell(table, rows, col, value):
    for r in rows:
        table.setItem(r, col, value)
