import sys
sys.path.append('/home/scexao/steph/control-code')

import apiMEMsControl 
import chipMountControl 

from control_buttons_ui import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt



def preprocessing(gui):
    gui.list_segments.setVisible(False)


def triggers(gui, mems, mount):

    '''
    Test we have connection with MEMs and mount
    '''
    # gui.pushButton_numActuators.clicked.connect(
    #     lambda: numActuators(gui, mems))
    
    # gui.pushButton_setActuator.clicked.connect(
    #     lambda: setActuator(gui, mems))
    
    # gui.pushButton_getActuator.clicked.connect(
    #     lambda: getActuator(gui, mems))
    
    # gui.pushButton_getPos.clicked.connect(
    #     lambda: getPos(gui, mount))

    # gui.pushButton_setPos.clicked.connect(
    #     lambda: setPos(gui, mount))


    ### Segment list ###
    # Replace the original focusInEvent with the new one
    gui.text_segments.focusInEvent = lambda event: focusInEvent(gui)
    gui.text_segments.focusOutEvent = lambda event: test_segment_format(gui.text_segments.text(), gui.text_segments)

    ### MEMs control buttons ###
    gui.pushButton_flattenMEMs.clicked.connect(
        lambda: flatten(gui, mems))


    # ### Manual control buttons ###
    gui.pushButton_x_up.clicked.connect(
        lambda: x_up(gui, mount))
    gui.pushButton_x_down.clicked.connect(
        lambda: x_down(gui, mount))
    gui.pushButton_y_up.clicked.connect(
        lambda: y_up(gui, mount))
    gui.pushButton_y_down.clicked.connect(
        lambda: y_down(gui, mount))
    gui.pushButton_z_up.clicked.connect(
        lambda: z_up(gui, mount))
    gui.pushButton_z_down.clicked.connect(
        lambda: z_down(gui, mount))
    gui.pushButton_yaw_up.clicked.connect(
        lambda: yaw_up(gui, mount))
    gui.pushButton_yaw_down.clicked.connect(
        lambda: yaw_down(gui, mount))
    gui.pushButton_roll_up.clicked.connect(
        lambda: roll_up(gui, mount))
    gui.pushButton_roll_down.clicked.connect(
        lambda: roll_down(gui, mount))
    gui.pushButton_pitch_up.clicked.connect(
        lambda: pitch_up(gui, mount))
    gui.pushButton_pitch_down.clicked.connect(  
        lambda: pitch_down(gui, mount))

    gui.pushButton_stop.clicked.connect(
        lambda: stop(mount))

    gui.pushButton_setSpeed.clicked.connect(
        lambda: setSpeed(gui, mount))
    gui.pushButton_getSpeed.clicked.connect(
        lambda: getSpeed(gui, mount))
    
    gui.pushButton_setOrigin.clicked.connect(
        lambda: set_origin(gui, mount))
    gui.pushButton_getOrigin.clicked.connect(
        lambda: get_origin(gui, mount))
    gui.pushButton_origin.clicked.connect(
        lambda: origin(gui, mount))
    
    
    gui. pushButton_piston_up.clicked.connect(
        lambda: pist_up(gui, mems))
    gui.pushButton_piston_down.clicked.connect(
        lambda: pist_down(gui, mems))
    gui.pushButton_tip_up.clicked.connect(
        lambda: tip_up(gui, mems))
    gui.pushButton_tip_down.clicked.connect(
        lambda: tip_down(gui, mems))
    gui.pushButton_tilt_up.clicked.connect(
        lambda: tilt_up(gui, mems))
    gui.pushButton_tilt_down.clicked.connect(
        lambda: tilt_down(gui, mems))



    # # ### Live cam checkbox ###
    # # gui.checkBox_livecam.stateChanged.connect(
    # #     lambda state, gui=gui: toggleLiveCam(gui, state))



    # ### Manual control checkboxes ###
    # gui.checkBox_manualMEMs.stateChanged.connect(
    #     lambda state: toggleMEMsEditable(gui, state))
    # gui.checkBox_manualMount.stateChanged.connect(
    #     lambda state: toggleMountEditable(gui, state))

    
    
    ### Set step sizes ###
    gui.text_pistStepSize.textChanged.connect(
        lambda text, le=gui.text_pistStepSize: on_text_changed(text, le))
    gui.text_ttStepSize.textChanged.connect(
        lambda text, le=gui.text_ttStepSize: on_text_changed(text, le))
    
    gui.text_mountStepSize_urad.textChanged.connect(
        lambda text, le=gui.text_mountStepSize_urad: on_text_changed(text, le))
    gui.text_mountStepSize_um.textChanged.connect(
        lambda text, le=gui.text_mountStepSize_um: on_text_changed(text, le))

    gui.table_mountPos_rpy.itemChanged.connect(on_item_changed)
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

def getPos(gui, mount):
    axis = 4
    pos = mount.get_pos(axis)
    gui.label_getPos.setText(str(pos))

def setPos(gui, mount):
    axis = 4
    pos = float(gui.text_setPos.text())
    mount.set_pos(axis, pos)

def setActuator(gui, mems):
    actuator = 0
    value = float(gui.text_setActuator.text())
    mems.set_actuator(actuator, value)

def getActuator(gui, mems):
    actuator = 0
    value = mems.get_actuator_data()
    gui.label_getActuator.setText(str(value[actuator]))

def setSpeed(gui, mount):
    speed = int(gui.text_setSpeed.text())
    axis = int(gui.text_axis.text())
    mount.set_speed(axis, speed)

def getSpeed(gui, mount):
    axis = int(gui.text_axis.text())
    speed = mount.get_speed(axis)
    gui.label_getSpeed.setText(str(speed))

def set_origin(gui, mount):
    axis = int(gui.text_axis.text())
    pattern = int(gui.text_setOrigin.text())
    mount.set_origin_pattern(axis, pattern)

def get_origin(gui, mount):
    axis = int(gui.text_axis.text())
    pattern = mount.get_origin_pattern(axis)
    gui.label_getOrigin.setText(str(pattern))

def origin(gui, mount):
    axis = int(gui.text_axis.text())
    mount.go_origin(axis)

    # No point doing this if you call it while mount still moving.
    # row = 0
    
    # if axis == 1:
    #     table = gui.table_mountPos_rpy
    #     col = 1
    # elif axis == 2:
    #     table = gui.table_mountPos_rpy
    #     col = 0
    # elif axis == 3:
    #     table = gui.table_mountPos_rpy
    #     col = 2
    # elif axis == 4:
    #     table = gui.table_mountPos_xyz
    #     col = 0
    # elif axis == 5:
    #     table = gui.table_mountPos_xyz
    #     col = 2
    # elif axis == 6:
    #     table = gui.table_mountPos_xyz
    #     col = 1

    
        # pos = mount.get_pos(axis)
        # update_cell(table, row, col, pos)

def stop(mount):
    mount.rstop()

def flatten(gui, mems):
    mems.flatten()
    for r in range(37):
        for c in range(3):
            gui.tab_memsPosition.setItem(r, c, QtWidgets.QTableWidgetItem('0.000'))

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

        '''
        psudeocode:
        1. check that it will be within limits
        2. send the command
        3. get the new position
        4. update the cell
        '''


        # If the value is a valid float, allow the change
        item.setText("{:.3f}".format(float_value))  # Convert to 3 decimal places if it's a float
    except ValueError:
        # If the entered value is not a float, prevent the change
        
        '''
        psuedocode:
        1. get the previous cell value
        2. set the cell value to the previous value
        '''
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



def test_segment_format(text, le):

    '''
    Copilot worte this code
    '''
    default = "E.g. 0, 4, 8"

    if not text:
        le.setText(default)
    else:
        try:
            # Check if the string is in the format of an array
            segments = [int(s.strip()) for s in text.split(',')]
            print(segments)
            # If the format is correct, set the text to the input text
            le.setText(text)
        except ValueError:
            le.setText(default)
            print("Invalid format. Please enter numbers separated by commas.")

# Modify the focusInEvent to not clear the text if it's in the correct format
def focusInEvent(gui):

    segments = get_segments(gui)

    if segments is None:
        gui.text_segments.setText('')

def get_segments(gui):

    try:
        text_segments = gui.text_segments.text()
        segments = [int(s.strip()) for s in text_segments.split(',')]
        return segments
    except ValueError:
        print("No segment given.")
        return None
    

def pist_up(gui, mems):
    
    segments = get_segments(gui)

    if segments is not None:

        stepsize = check_stepSize(gui.text_pistStepSize)

        if stepsize is not None:
            row = segments
            col = 0
            table = gui.tab_memsPosition

            for r in row:
                segment = r
                pist = float(table.item(r, 0).text())
                tip = float(table.item(r, 1).text())
                tilt = float(table.item(r, 2).text())
                newpist = pist + stepsize

                mems.set_segment(segment, newpist, tip, tilt)
                update_cell(table, r, col, newpist)

'''
Pseudocode:
Get the segment(s)
Get the current piston position
Add the step size to the current position
Set the new position
'''
def pist_down(gui, mems):

    segments = get_segments(gui)

    if segments is not None:

        stepsize = check_stepSize(gui.text_pistStepSize)

        if stepsize is not None:
            row = segments
            col = 0
            table = gui.tab_memsPosition

            for r in row:
                segment = r
                pist = float(table.item(r, 0).text())
                tip = float(table.item(r, 1).text())
                tilt = float(table.item(r, 2).text())
                newpist = pist - stepsize

                mems.set_segment(segment, newpist, tip, tilt)
                update_cell(table, r, col, newpist)


def tip_up(gui, mems):

    segments = get_segments(gui)

    if segments is not None:

        stepsize = check_stepSize(gui.text_ttStepSize)

        if stepsize is not None:
            row = segments
            col = 1
            table = gui.tab_memsPosition

            for r in row:
                segment = r
                pist = float(table.item(r, 0).text())
                tip = float(table.item(r, 1).text())
                tilt = float(table.item(r, 2).text())
                newtip = tip + stepsize

                mems.set_segment(segment, pist, newtip, tilt)
                update_cell(table, r, col, newtip)

def tip_down(gui, mems):

    segments = get_segments(gui)

    if segments is not None:

        stepsize = check_stepSize(gui.text_ttStepSize)

        if stepsize is not None:
            row = segments
            col = 1
            table = gui.tab_memsPosition

            for r in row:
                segment = r
                pist = float(table.item(r, 0).text())
                tip = float(table.item(r, 1).text())
                tilt = float(table.item(r, 2).text())
                newtip = tip - stepsize

                mems.set_segment(segment, pist, newtip, tilt)
                update_cell(table, r, col, newtip)

def tilt_up(gui, mems):
    
    segments = get_segments(gui)

    if segments is not None:

        stepsize = check_stepSize(gui.text_ttStepSize)

        if stepsize is not None:
            row = segments
            col = 2
            table = gui.tab_memsPosition

            for r in row:
                segment = r
                pist = float(table.item(r, 0).text())
                tip = float(table.item(r, 1).text())
                tilt = float(table.item(r, 2).text())
                newtilt = tilt + stepsize

                mems.set_segment(segment, pist, tip, newtilt)

                update_cell(table, r, col, newtilt)


def tilt_down(gui, mems):

    segments = get_segments(gui)

    if segments is not None:
            
            stepsize = check_stepSize(gui.text_ttStepSize)
    
            if stepsize is not None:
                row = segments
                col = 2
                table = gui.tab_memsPosition
    
                for r in row:
                    segment = r
                    pist = float(table.item(r, 0).text())
                    tip = float(table.item(r, 1).text())
                    tilt = float(table.item(r, 2).text())
                    newtilt = tilt - stepsize
    
                    mems.set_segment(segment, pist, tip, newtilt)
                    update_cell(table, r, col, newtilt)



def x_up(gui, mount):
    stepsize = check_stepSize(gui.text_mountStepSize_um)

    if stepsize is not None:
        table = gui.table_mountPos_xyz
        row = 0
        col = 0
        axis = 4

        # # This commented code is to use when not connected to the mount
        # pos = float(table.item(0, 0).text())
        # newpos = pos + stepsize
        # update_cell(table, row, col, newpos)

        # Uncomment all of below when actuatlly connected
        pos = mount.get_pos(axis)
        newpos = int(pos + stepsize)
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
        row = 0
        col = 0
        axis = 4

        pos = mount.get_pos(axis)
        newpos = int(pos - stepsize)
        mount.set_pos(axis, newpos)
        updated_pos = mount.get_pos(axis)
        update_cell(table, row, col, updated_pos)


def y_up(gui, mount):

    stepsize = check_stepSize(gui.text_mountStepSize_um)
    if stepsize is not None:
        table = gui.table_mountPos_xyz
        row = 0
        col = 1
        axis = 6

        pos = mount.get_pos(axis)
        newpos = int(pos + stepsize)
        mount.set_pos(axis, newpos)
        
        updated_pos = mount.get_pos(axis)
        update_cell(table, row, col, updated_pos)


def y_down(gui, mount):
    
    stepsize = check_stepSize(gui.text_mountStepSize_um)
    if stepsize is not None:
        table = gui.table_mountPos_xyz
        row = 0
        col = 1
        axis = 6

        pos = mount.get_pos(axis)
        newpos = int(pos - stepsize)
        mount.set_pos(axis, newpos)
        
        updated_pos = mount.get_pos(axis)
        update_cell(table, row, col, updated_pos)

def z_up(gui, mount):
    
    stepsize = check_stepSize(gui.text_mountStepSize_um)
    if stepsize is not None:
        table = gui.table_mountPos_xyz
        row = 0
        col = 2
        axis = 5

        pos = mount.get_pos(axis)
        newpos = int(pos + stepsize)
        mount.set_pos(axis, newpos)
        
        updated_pos = mount.get_pos(axis)
        update_cell(table, row, col, updated_pos)

def z_down(gui, mount):
    
    stepsize = check_stepSize(gui.text_mountStepSize_um)
    if stepsize is not None:
        table = gui.table_mountPos_xyz
        row = 0
        col = 2
        axis = 5

        pos = mount.get_pos(axis)
        newpos = int(pos - stepsize)
        mount.set_pos(axis, newpos)
        
        updated_pos = mount.get_pos(axis)
        update_cell(table, row, col, updated_pos)


def roll_up(gui, mount):
    
    stepsize = check_stepSize(gui.text_mountStepSize_urad)
    if stepsize is not None:
        table = gui.table_mountPos_rpy
        row = 0
        col = 0
        axis = 2

        # # This commented code is to use when not connected to the mount
        # pos = float(table.item(0, 0).text())
        # newpos = pos + stepsize
        # update_cell(table, row, col, newpos)

        pos = mount.get_pos(axis)
        newpos = int(pos + stepsize)
        mount.set_pos(axis, newpos)
        updated_pos = mount.get_pos(axis)
        update_cell(table, row, col, updated_pos)


def roll_down(gui, mount):
    
    stepsize = check_stepSize(gui.text_mountStepSize_urad)
    if stepsize is not None:
        table = gui.table_mountPos_rpy
        row = 0
        col = 0
        axis = 2

        pos = mount.get_pos(axis)
        newpos = int(pos - stepsize)
        mount.set_pos(axis, newpos)
        updated_pos = mount.get_pos(axis)
        update_cell(table, row, col, updated_pos)


def pitch_up(gui, mount):
    
    stepsize = check_stepSize(gui.text_mountStepSize_urad)
    if stepsize is not None:
        table = gui.table_mountPos_rpy
        row = 0
        col = 1
        axis = 1

        pos = mount.get_pos(axis)
        newpos = int(pos + stepsize)
        mount.set_pos(axis, newpos)
        updated_pos = mount.get_pos(axis)
        update_cell(table, row, col, updated_pos)


def pitch_down(gui, mount):
    
    stepsize = check_stepSize(gui.text_mountStepSize_urad)
    if stepsize is not None:
        table = gui.table_mountPos_rpy
        row = 0
        col = 1
        axis = 1

        pos = mount.get_pos(axis)
        newpos = int(pos - stepsize)
        mount.set_pos(axis, newpos)
        updated_pos = mount.get_pos(axis)
        update_cell(table, row, col, updated_pos)


def yaw_up(gui, mount):
    
    stepsize = check_stepSize(gui.text_mountStepSize_urad)
    if stepsize is not None:
        table = gui.table_mountPos_rpy
        row = 0
        col = 2
        axis = 3

        pos = mount.get_pos(axis)
        newpos = int(pos + stepsize)
        mount.set_pos(axis, newpos)
        updated_pos = mount.get_pos(axis)
        update_cell(table, row, col, updated_pos)


def yaw_down(gui, mount):

    stepsize = check_stepSize(gui.text_mountStepSize_urad)
    if stepsize is not None:
        table = gui.table_mountPos_rpy
        row = 0
        col = 2
        axis = 3

        pos = mount.get_pos(axis)
        newpos = int(pos - stepsize)
        mount.set_pos(axis, newpos)
        updatedpos = mount.get_pos(axis)
        update_cell(table, row, col, updatedpos)


def update_cell(table, r, col, value):
    item = QtWidgets.QTableWidgetItem("{:.3f}".format(value))
    table.setItem(r, col, item)


def get_checked_states(gui):
    # Get the checked state of each item in the QListWidget
    checked_states = []

    for i in range(gui.list_segments.count()):
        item = gui.list_segments.item(i)
        if item.checkState() == Qt.Checked:
            checked_states.append(int(item.text()))

    return checked_states