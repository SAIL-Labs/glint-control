## Todo:
# - make the table editable and usable
# - enable functionality using baselines not just individual segments (done?)
# - enable function such that all segments except the usable ones move (done?)
# - make apapane view live
# - implement optimisation scans into gui
# - allow multi-frame saving from gui (done?)
# - implement tip/tilt in simulation mode



'''
This file provides funtionality to the GUI buttons. It is imported into the main GUI file, run_GUI.py. Where addditionalcomputation is required (e.g. null scan, chip simulator), the functions are called from this file.
'''
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
import functions
# import optimisationscansnight1
import pistscan
import ttscan
import numpy as np
from astropy.io import fits
import traceback

PREVIOUS_VALUES = {
    'tab_memsPosition_base': {(row, col): 0 for row in range(3) for col in range(3)},
    'tab_memsPosition_seg': {(row, col): 0 for row in range(37) for col in range(3)},
    'table_mountPos_xyz': {(row, col): 0 for row in range(1) for col in range(3)},
    'table_mountPos_rpy': {(row, col): 0 for row in range(1) for col in range(3)}
}

APERTURE_NUMBERS = [11, 20, 31]




def triggers(gui, mems, mount, cameras):

    ### Segment list ###
    # Replace the original focusInEvent with the new one
    gui.text_segments.focusInEvent = lambda event: focusInEvent_segments(gui)
    gui.text_segments.focusOutEvent = lambda event: test_segmentls_format(gui.text_segments.text(), gui.text_segments)


    ### Manual control checkboxes ###
    gui.checkBox_manualMEMs_base.stateChanged.connect(
        lambda state: toggleMEMsEditable(gui, state))
    gui.checkBox_manualMEMs_seg.stateChanged.connect(
        lambda state: toggleMEMsEditable(gui, state))
    gui.checkBox_manualMount.stateChanged.connect(
        lambda state: toggleMountEditable(gui, state))

    
    # We want this wrapped in a try-except block because tehre are various errors the mount can 
    # encounter and we don't want it to cause the entire GUI (and thus mems) to quit
    try:

        gui.pushButton_TTscan.clicked.connect(
            lambda: ttscan.tiptiltscan(mems, cameras))
        gui.pushButton_pistonscan.clicked.connect(
            lambda: pistscan.pistonscan(mems, cameras))
        

        ### MOUNT control buttons ###
        gui.pushButton_x_up.clicked.connect(
            lambda: move_mount(gui, mount, 'x', 'up'))
        gui.pushButton_x_down.clicked.connect(
            lambda: move_mount(gui, mount, 'x', 'down'))
        gui.pushButton_y_up.clicked.connect(
            lambda: move_mount(gui, mount, 'y', 'up'))
        gui.pushButton_y_down.clicked.connect(
            lambda: move_mount(gui, mount, 'y', 'down'))
        gui.pushButton_z_up.clicked.connect(
            lambda: move_mount(gui, mount, 'z', 'up'))
        gui.pushButton_z_down.clicked.connect(
            lambda: move_mount(gui, mount, 'z', 'down'))
        gui.pushButton_yaw_up.clicked.connect(
            lambda: move_mount(gui, mount, 'yaw', 'up'))
        gui.pushButton_yaw_down.clicked.connect(
            lambda: move_mount(gui, mount, 'yaw', 'down'))
        gui.pushButton_roll_up.clicked.connect(
            lambda: move_mount(gui, mount, 'roll', 'up'))
        gui.pushButton_roll_down.clicked.connect(
            lambda: move_mount(gui, mount, 'roll', 'down'))
        gui.pushButton_pitch_up.clicked.connect(
            lambda: move_mount(gui, mount, 'pitch', 'up'))
        gui.pushButton_pitch_down.clicked.connect(
            lambda: move_mount(gui, mount, 'pitch', 'down'))
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
        gui.pushButton_getpositions.clicked.connect(
            lambda: get_mountpos(gui, mount))
        gui.pushButton_stop.clicked.connect(
            lambda: stop(mount))
    
    
    
        ### MEMs control buttons ###
        gui. pushButton_piston_up_base.clicked.connect(
            lambda: move_mems(gui, mems, memsMode = 'base', command = 'piston', direction = 'up'))
        gui.pushButton_piston_down_base.clicked.connect(
            lambda: move_mems(gui, mems, memsMode = 'base', command = 'piston', direction = 'down'))
        gui.pushButton_tip_up_base.clicked.connect(
            lambda: move_mems(gui, mems, memsMode = 'base', command = 'tip', direction = 'up'))
        gui.pushButton_tip_down_base.clicked.connect(
            lambda: move_mems(gui, mems, memsMode = 'base', command = 'tip', direction = 'down'))
        gui.pushButton_tilt_up_base.clicked.connect(
            lambda: move_mems(gui, mems, memsMode = 'base', command = 'tilt', direction = 'up'))
        gui.pushButton_tilt_down_base.clicked.connect(
            lambda: move_mems(gui, mems, memsMode = 'base', command = 'tilt', direction = 'down'))
        gui. pushButton_piston_up_seg.clicked.connect(
            lambda: move_mems(gui, mems, memsMode = 'seg', command = 'piston', direction = 'up'))
        gui.pushButton_piston_down_seg.clicked.connect(
            lambda: move_mems(gui, mems, memsMode = 'seg', command = 'piston', direction = 'down'))
        gui.pushButton_tip_up_seg.clicked.connect(
            lambda: move_mems(gui, mems, memsMode = 'seg', command = 'tip', direction = 'up'))
        gui.pushButton_tip_down_seg.clicked.connect(
            lambda: move_mems(gui, mems, memsMode = 'seg', command = 'tip', direction = 'down'))
        gui.pushButton_tilt_up_seg.clicked.connect(
            lambda: move_mems(gui, mems, memsMode = 'seg', command = 'tilt', direction = 'up'))
        gui.pushButton_tilt_down_seg.clicked.connect(
            lambda: move_mems(gui, mems, memsMode = 'seg', command = 'tilt', direction = 'down'))
        
        gui.pushButton_flattenMEMs_base.clicked.connect(
            lambda: flatten(mems, table = gui.tab_memsPosition_base))
        gui.pushButton_flattenMEMs_seg.clicked.connect(
            lambda: flatten(mems, table = gui.tab_memsPosition_seg))
            
        gui.pushButton_zeroMEMS_seg.clicked.connect(
            lambda: sendzeros(mems, table = gui.tab_memsPosition_seg))
        gui.pushButton_zeroMEMS_base.clicked.connect(
            lambda: sendzeros(mems, table = gui.tab_memsPosition_base))
        
        
        
        gui.pushButton_save.clicked.connect(
            lambda: save_frames(gui, cameras))
        
        
        ### Spectral Simulator ###
        # gui.checkBox_simMode.stateChanged.connect(
        #     lambda state: toggleLiveCam(gui, state))
        
        
        ### Set step sizes ###
        gui.text_pistStepSize_base.textChanged.connect(
            lambda text, le=gui.text_pistStepSize_base: on_text_changed(text, le))
        gui.text_ttStepSize_base.textChanged.connect(
            lambda text, le=gui.text_ttStepSize_base: on_text_changed(text, le))
        
        gui.text_mountStepSize_urad.textChanged.connect(
            lambda text, le=gui.text_mountStepSize_urad: on_text_changed(text, le))
        gui.text_mountStepSize_um.textChanged.connect(
            lambda text, le=gui.text_mountStepSize_um: on_text_changed(text, le))

        
        # gui.tab_memsPosition_base.itemChanged.connect(
        #     lambda item, device = mems, table=gui.tab_memsPosition_base: on_item_changed(item, device, table))
        # gui.tab_memsPosition_seg.itemChanged.connect(
        #     lambda item, device = mems, table=gui.tab_memsPosition_seg: on_item_changed(item, device, table))
        
        # gui.table_mountPos_rpy.itemChanged.connect(
        #     lambda item, device = mount, table=gui.table_mountPos_rpy: on_item_changed(item, device, table))
        # gui.table_mountPos_xyz.itemChanged.connect(
        #     lambda item, device = mount, table=gui.table_mountPos_xyz: on_item_changed(item, device, table))
        
    
    except Exception as e:
        print("Error:", e)

### GENERAL FUNCTIONS ###

def update_cell(table, r, col, value):

    # Delegate ensures that when a user edits the cell, the input is formatted and displayed as an integer without decimals.
    item = QtWidgets.QTableWidgetItem(str(value))

    table.setItem(r, col, item)

def get_checked_states(gui):
    # Get the checked state of each item in the QListWidget
    checked_states = []

    for i in range(gui.list_segments.count()):
        item = gui.list_segments.item(i)
        if item.checkState() == Qt.Checked:
            checked_states.append(int(item.text()))

    return checked_states

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

def on_item_changed(item, device, table):
    '''    
    psudeocode:
        1. get the new value
        2. if the value is not a float, prevent the change
        3. else, continue
        5. send the command
        6. get the new position
        7. update the cell
    '''
    text = item.text()
    row = item.row()
    col = item.column()
    table_name = table.objectName()
    

    try:
        float_value = float(text)
        new_value = float_value

        if device is not None:
            move(device, table, row, col, new_value)

        # update previous value
        PREVIOUS_VALUES[table_name][(row, col)] = new_value

        # Prevent the cellChanged signal from being triggered otherwise previous value will be overwritten
        table.blockSignals(True)
        item.setText("{:.3f}".format(new_value))  # Convert to 3 decimal places if it's a float
        table.blockSignals(False)

    except ValueError: # If the entered value is not a float, prevent the change
        previous_table = PREVIOUS_VALUES[table_name]
        prev_value = previous_table.get((row, col), 0)

        table.blockSignals(True)
        item.setText("{:.3f}".format(prev_value))
        table.blockSignals(False)

def check_stepSize(stepsize):
   
    try:
        step = stepsize.text()
        step = float(step)
        return step
    except ValueError:
        return None

def move(device, table, row, col, value):

    '''
    pseudocode:
    mems:
        1. find the segment
        2. check the limits
        3. set the segment
        4. get the new position
    mount:
        1. get axis (p = 1, r = 2, y = 3, x = 4, z = 5, y = 6)
        2. check the limits
        3. set the position
        4. get the new position
    '''
    
    if table.objectName() == 'tab_memsPosition_seg':
        
        segment = row
        piston = float(table.item(row, 0).text())
        tip = float(table.item(row, 1).text())
        tilt = float(table.item(row, 2).text())

        device.set_segment(segment, piston, tip, tilt)

    elif table.objectName() == 'tab_memsPosition_base':
        segment = APERTURE_NUMBERS[row]

        piston = float(table.item(row, 0).text())
        tip = float(table.item(row, 1).text())
        tilt = float(table.item(row, 2).text())

        device.set_segment(segment, piston, tip, tilt)
        
    elif table.objectName() == 'table_mountPos_xyz':
        if col == 0:
            axis = 4
        elif col == 1:
            axis = 6
        elif col == 2:
            axis = 5
        
        value  = int(value)
        
        device.set_pos(axis, value)
    
    elif table.objectName() == 'table_mountPos_rpy':
        if col == 0:
            axis = 2
        elif col == 1:
            axis = 1
        elif col == 2:
            axis = 3

        value  = int(value)
        
        device.set_pos(axis, value)

    


### MOUNT FUNCTIONS ###

def toggleMountEditable(gui, state):
    if state == 2:  # 2 corresponds to checked state
        gui.widget_manualMount_inner.setEnabled(True)
        gui.table_mountPos_rpy.setEditTriggers(QtWidgets.QTableWidget.AllEditTriggers)
        gui.table_mountPos_xyz.setEditTriggers(QtWidgets.QTableWidget.AllEditTriggers)
    else:
        gui.widget_manualMount_inner.setEnabled(False)
        gui.table_mountPos_rpy.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        gui.table_mountPos_xyz.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

def setSpeed(gui, mount):
    if mount is None:
        print("No mount connected.")
        return

    try:
        speed = int(gui.text_setSpeed.text())
    except ValueError:
        print("Invalid speed: must be an integer between 1 (slowest) and 6 (fastest).")
        return
    
    try:
        axis = int(gui.text_axis.text())
    except ValueError:
        print("Invalid axis number: 1 (pitch), 2 (roll), 3 (yaw), 4 (x), 5 (z), 6 (y).")
        return
    
    try:
        mount.set_speed(axis, speed)

    except Exception as e:
        print("Error setting speed:", e)
        return

def getSpeed(gui, mount):

    if mount is None:
        print("No mount connected.")
        return

    try:
        axis = int(gui.text_axis.text())
    except ValueError:
        print("Invalid axis number: 1 (pitch), 2 (roll), 3 (yaw), 4 (x), 5 (z), 6 (y).")
        return
    
    try:
        speed = mount.get_speed(axis)
        gui.label_getSpeed.setText(str(speed))
        
    except Exception as e:
        print("Error getting speed:", e)
        return

def set_origin(gui, mount):

    print('Disabled origin function.')

    # if mount is None:
    #     print("No mount connected.")
    #     return

    # try:
    #     axis = int(gui.text_axis.text())
    # except ValueError:
    #     print("Invalid axis number: 1 (pitch), 2 (roll), 3 (yaw), 4 (x), 5 (z), 6 (y).")
    #     return
    
    # try:
    #     pattern = int(gui.text_setOrigin.text())
    # except ValueError:
    #     print("Invalid origin pattern: 3 (clockwise), 4 (counter-clockwise).")
    #     return
    
    # try:
    #     mount.set_origin_pattern(axis, pattern)

    # except Exception as e:
    #     print("Error setting origin:", e)
    #     return

def get_origin(gui, mount):

    print("Disabled origin function.")
    # if mount is None:
    #     print("No mount connected.")
    #     return

    # try:
    #     axis = int(gui.text_axis.text())
    # except ValueError:
    #     print("Invalid axis number: 1 (pitch), 2 (roll), 3 (yaw), 4 (x), 5 (z), 6 (y).")
    #     return
    
    # try:
    #     pattern = mount.get_origin_pattern(axis)
    #     gui.label_getOrigin.setText(str(pattern))
    # except Exception as e:
    #     print("Error getting origin pattern:", e)
    #     return



def preorigin_checks():

    '''
    check the following:
    1) origin pattern is correct
    2) position relative to origin is good to proceed with origining
    3) if not, a pop-up message should appear
    '''
    pass



def origin(gui, mount):

    print('Disabled origin function.')
    # if mount is None:
    #     print("No mount connected.")
    #     return

    # try:
    #     axis = int(gui.text_axis.text())
    # except ValueError:
    #     print("Invalid axis number: 1 (pitch), 2 (roll), 3 (yaw), 4 (x), 5 (z), 6 (y).")
    #     return
    
    # try:
    #     mount.go_origin(axis)
        
    # except Exception as e:
    #     print("Error going to origin:", e)
    #     return



def stop(mount):

    if mount is None:
        print("No mount connected.")
        return
    
    try:
        mount.rstop()
    except Exception as e:
        print("Error stopping mount:", e)
        return


'''
Pseudocode:
Get the current mount position
Add the step size to the current position
Set the new position
'''
def unpack_mounttable(gui, command):

    if command == 'x':
        table = gui.table_mountPos_xyz
        row = 0
        col = 0
        axis = 4
        stepsize = check_stepSize(gui.text_mountStepSize_um) # get stepsize and check if it's a float
    elif command == 'y':
        table = gui.table_mountPos_xyz
        row = 0
        col = 1
        axis = 6
        stepsize = check_stepSize(gui.text_mountStepSize_um)
    elif command == 'z':
        table = gui.table_mountPos_xyz
        row = 0
        col = 2
        axis = 5
        stepsize = check_stepSize(gui.text_mountStepSize_um)
    elif command == 'roll':
        table = gui.table_mountPos_rpy
        row = 0
        col = 0
        axis = 2
        stepsize = check_stepSize(gui.text_mountStepSize_urad)
    elif command == 'pitch':
        table = gui.table_mountPos_rpy
        row = 0
        col = 1
        axis = 1
        stepsize = check_stepSize(gui.text_mountStepSize_urad)
    elif command == 'yaw':
        table = gui.table_mountPos_rpy
        row = 0
        col = 2
        axis = 3
        stepsize = check_stepSize(gui.text_mountStepSize_urad)
    else:
        print("Invalid command.")
        return

    return (table, row, col, axis, stepsize)


def move_mount(gui, mount, command, direction):

    # Get the table and the row and column of the cell to be updated
    (table, row, col, axis, stepsize) = unpack_mounttable(gui, command)

    if stepsize is not None:

        ### MAYBE CHANGE THIS TO IF SIMULATION CHECKBOX IS TICKED
        if mount is not None:   # i.e. if in simulation mode and can't connect to the mount
        #     # Get the current position from the table
        #     pos = float(table.item(row, col).text())

        #     # Add the step size to the current position

        #     if direction == 'up':
        #         updated_pos = pos + stepsize
        #     elif direction == 'down':
        #         updated_pos = pos - stepsize
        #     else:
        #         print("Invalid direction.")
        #         return
            
        # else:

            # Get the current position of the stage
            pos = mount.get_pos(axis)

            # Add the step size to the current position
            if direction == 'up':
                newpos = int(pos + stepsize)
            elif direction == 'down':
                newpos = int(pos - stepsize)
            else:
                print("Invalid direction.")
                return

            # Set the new position
            mount.set_pos(axis, newpos)
    else:
        print("Mount step size not given.")

def get_mountpos(gui, mount):

    if mount is None:
        print("No mount connected.")
        return
    
    axes = ['x', 'y', 'z', 'pitch', 'roll', 'yaw']

    for ax in axes:
        (table, row, col, axis, _) = unpack_mounttable(gui, ax)
        updated_pos = mount.get_pos(axis)

        update_cell(table, row, col, updated_pos)       



### MEMs FUNCTIONS ###

def flatten(mems, table):

    ## IMPORTANT: This does not send the ptt to zero, so the table technically shouldn't be zero.
    # Check is connected to mems, in which case, flatten it
    if mems is not None: 
        mems.flatten()

    else:
        print("No MEMs connected.")
    
    # Note that we don't get the position of the mems, we assume it's doing what it should. Also note that the flatten command 
    # remaps the positions to 0, but the flatfile itself is not a ann array of zeros.
    for r in range(37):
        for c in range(3):
            update_cell(table, r, c, 0)
    
def sendzeros(mems, table):
    ## IMPORTANT: This does not send the ptt to zero, just the volts, so the table technically shouldn't be zero.
    # Check is connected to mems, in which case, send zeros
    if mems is not None: 
        mems.sendzeros()


    else:
        print("No MEMs connected.")
    
    # Note that we don't get the position of the mems, we assume it's doing what it should. Also note that the flatten command 
    # remaps the positions to 0, but the flatfile itself is not a ann array of zeros.
    for r in range(37):
        for c in range(3):
            update_cell(table, r, c, 0)




def toggleList(gui):
    # Toggle the visibility of the list widget
    gui.list_segments.setVisible(not gui.list_segments.isVisible())
    # gui.list_segments.raise_()

# def setTableEditable(table, editable):
#     if editable:
#         table.setEditTriggers(QtWidgets.QTableWidget.AllEditTriggers)
#     else:
#         table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
     
def toggleMEMsEditable(gui, state):
    '''
    This could be generalised but my brain hurts
    '''

    if state == 2:  # 2 corresponds to checked state
        gui.widget_manualMEMS_inner_base.setEnabled(True)
        gui.widget_manualMEMS_inner_seg.setEnabled(True)
        gui.tab_memsPosition_seg.setEditTriggers(QtWidgets.QTableWidget.AllEditTriggers)
        gui.tab_memsPosition_base.setEditTriggers(QtWidgets.QTableWidget.AllEditTriggers)
    else:
        gui.widget_manualMEMS_inner_base.setEnabled(False)
        gui.widget_manualMEMS_inner_seg.setEnabled(False)
        gui.tab_memsPosition_base.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        gui.tab_memsPosition_base.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)


def test_segmentls_format(text, le):

    '''
    Copilot wrote this code
    '''
    default = "E.g. 0, 4"

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
def focusInEvent_segments(gui):

    segments = get_segments(gui)

    if segments is None:
        gui.text_segments.setText('')

def focusInEvent_mems(gui):
    pass

    
def get_segments(gui):

    try:
        text_segments = gui.text_segments.text()
        segments = [int(s.strip()) for s in text_segments.split(',')]
        return segments
    except ValueError:
        print("No segment given.")
        return None
        
def get_baselines(gui):

    baseline = gui.comboBox_baselines.currentText()

    # Convert the baseline array into a list of integers
    try:
        baseline_list = [int(s.strip()) for s in baseline.split(',')]
    
    except ValueError:
        print("Invalid baseline format.")
        return

    if gui.radioButton_seg1.isChecked():
        aperture = baseline_list[0]
    elif gui.radioButton_seg2.isChecked():
        aperture = baseline_list[1]
    else:
        print('No segment selected.')
        return

    segments = [aperture] # Subtract 1 to get the correct index, put it in a list to match the format of the other functions

    return segments

def unpack_mems(gui, memsMode, command):

    if memsMode == 'base':
        if command == 'piston':
            stepsize = check_stepSize(gui.text_pistStepSize_base)
            col = 0
        elif command == 'tip':
            stepsize = check_stepSize(gui.text_ttStepSize_base)
            col = 1
        elif command == 'tilt':
            stepsize = check_stepSize(gui.text_ttStepSize_base)
            col = 2
        else:
            print('Invalid command.')
            return
    elif memsMode == 'seg':
        if command == 'piston':
            stepsize = check_stepSize(gui.text_pistStepSize_seg)
            col = 0
        elif command == 'tip':
            stepsize = check_stepSize(gui.text_ttStepSize_seg)
            col = 1
        elif command == 'tilt':
            stepsize = check_stepSize(gui.text_ttStepSize_seg)
            col = 2
        else:
            print('Invalid command.')
            return

    return (stepsize, col)



def move_mems(gui, mems, memsMode, command, direction): # mems mode refers to if you use segments or baselines

    # Initialise the table, stepsize, and segments based on the mems mode i.e. 'base' (uses a selected baseline) or 'seg' (uses segment numbers)
    if memsMode == 'base':
        segments = get_baselines(gui)
    elif memsMode == 'seg':
        segments = get_segments(gui)
    else:
        print('Invalid mems mode.')
        return
    
    if segments is None: 
        # If no segments are given, return
        return
    
    # Main table used to get pistons from and update pistons to
    main_table = gui.tab_memsPosition_seg
    (stepsize, col) = unpack_mems(gui, memsMode, command)

    # Make sure the stepsize exists
    if stepsize is not None:

        # 37 will select all segments, -1 will select all segments except usable ones
        if 37 in segments:
            segments = list(range(37))
        elif -1 in segments:
            segments = list(range(37))

            # remove the relevant segments
            for aperturenum in APERTURE_NUMBERS:
                segments.remove(aperturenum)


        # Go through each segment selected to change the piston value
        for segment in segments:
            if segment < 0 or segment > 36:
                print('Incorrect segment number')
                return

            # Get the old piston value
            oldvalue = float(main_table.item(segment, col).text())

            # Calculate the new piston value 
            if direction == 'up':
                newvalue = oldvalue + stepsize
            elif direction == 'down':
                newvalue = oldvalue - stepsize
            
            # Send the new piston value to the MEMs
            if not gui.checkBox_simMode.isChecked() and mems is not None:  # if not in simulation mode and we have properly opened the MEMS, move a segment
                pist = float(main_table.item(segment, 0).text())
                tip = float(main_table.item(segment, 1).text())
                tilt = float(main_table.item(segment, 2).text())

                tiprad = tip/1000
                tiltrad = tilt/1000

                try:
                    error = mems.set_segment(segment, pist, tiprad, tiltrad) 

                    if error == -1:
                        print("No update to table.")
                        return
                except Exception:
                    traceback.print_exc()
                    return
                    
            # Update both tables with the new piston value
            update_cell(main_table, segment, col, newvalue)

            # Find the index of the segment in the table i.e. instead of 1,3,9 it would be 0,1,2
            if segment in APERTURE_NUMBERS:
                s = APERTURE_NUMBERS.index(segment)
                update_cell(gui.tab_memsPosition_base, s, col, newvalue)
            
            
            
        # Update the spectra if in simulation mode
        if gui.checkBox_simMode.isChecked():
            pistCol = 0
            pistons = np.array([float(main_table.item(segment, pistCol).text()) for segment in APERTURE_NUMBERS])
            functions.update_spectra(gui, pistons = pistons)
        
    else:
        print("MEMS step size not given.")



from datetime import datetime
def save_frames(gui, cameras):

    path = gui.text_path.text()
    
    checkboxes = [gui.checkBox_apapane, gui.checkBox_palila, gui.checkBox_pupil, gui.checkBox_focal]
    camnames = ['apapane', 'palila', 'glint_pupil', 'glint_focal']

    for idx, box in enumerate(checkboxes):
        if box.isChecked():

            if cameras is None:  # Are the cameras initialised or is this running locally
                frame = np.zeros((4,4))
            elif camnames[idx] == 'apapane':  # Apapane save data works slightly different to accomodate for multiple saves
                
                try: 
                    numframes = int(gui.text_numframes.text())
                    frame = cameras[idx].multi_recv_data(numframes)
                except ValueError:
                    numframes = 1 # force at least one frame to be saved
                    gui.text_numframes.setText(str(numframes))
                    print('Number of apapane frames to save must be an integer.')
                    return
            
            else:  # Save a single frame
                frame = cameras[idx].get_data()      
            
            dt = str(datetime.now())
            dt = dt.replace(' ', '_')

            if gui.text_filename.text() == "":  # i.e. if no filename was given in the gui, make a filename that saves it as a timestamp
                filename = camnames[idx] + '_' + dt 
            else:
                filename = gui.text_filename.text()

            try:
                # Save data as a fits file
                hdu = fits.PrimaryHDU(frame)
                hdul = fits.HDUList([hdu])
                hdul.writeto(path +'/'+ filename + '.fits', overwrite=False)
            except Exception as e:
                print('Save error occurred:', e)
        
