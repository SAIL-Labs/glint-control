from GUI_ui import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from apiMEMsControl import MEMS

def preprocessing(gui):
    gui.list_segments.setVisible(False)


def triggers(gui, mems):
    # gui.pushButton_save.clicked.connect(gui.save)

    ### MEMs control buttons ###
    gui.pushButton_flattenMEMs.clicked.connect(flatten)
    
    ### Manual control buttons ###
    gui.pushButton_x_up.clicked.connect(
        lambda: x_up(gui))
    gui.pushButton_y_up.clicked.connect(
        lambda: y_up(gui))
    gui.pushButton_z_up.clicked.connect(
        lambda: z_up(gui))
    gui.pushButton_yaw_up.clicked.connect(
        lambda: yaw_up(gui))
    gui.pushButton_roll_up.clicked.connect(
        lambda: roll_up(gui))
    gui.pushButton_pitch_up.clicked.connect(
        lambda: pitch_up(gui))
    gui.pushButton_x_down.clicked.connect(
        lambda: x_down(gui))
    gui.pushButton_y_down.clicked.connect(
        lambda: y_down(gui))
    gui.pushButton_z_down.clicked.connect(
        lambda: z_down(gui))
    gui.pushButton_yaw_down.clicked.connect(
        lambda: yaw_down(gui))
    gui.pushButton_roll_down.clicked.connect(
        lambda: roll_down(gui))
    gui.pushButton_piston_up.clicked.connect(
        lambda: piston_up(gui, mems))
    

    ### Toggle list widget ###
    gui.toggleButton_segments.clicked.connect(
        lambda: toggleList(gui))
    
    ### Live cam checkbox ###
    # gui.checkBox_livecam.stateChanged.connect(
    #     lambda state, gui=gui: toggleLiveCam(gui, state))



    ### Manual control checkboxes ###
    gui.checkBox_manualMEMs.stateChanged.connect(
        lambda state: toggleMEMsEditable(gui, state))
    gui.checkBox_manualMount.stateChanged.connect(
        lambda state: toggleMountEditable(gui, state))

    
    
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
    gui.table_mountPos_xyz.itemChanged.connect(on_item_changed)
    gui.tab_memsPosition.itemChanged.connect(on_item_changed)

def flatten():
    
    print("Flatten MEMs")

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
        print("Step value is not a float.")

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



def piston_up(gui, mems):
    stepsize = check_stepSize(gui.text_pistStepSize)
    if stepsize is not None:
        gui.list_segments


        '''
        Pseudocode:
        Get the segment(s)
        Get the current piston position
        Add the step size to the current position
        Set the new position
        '''


def x_up(gui):
    
    row = [0]
    col = 0
    action = "up"
    stepsize = gui.text_mountStepSize_um
    table = gui.table_mountPos_xyz
    manualCheckBox = gui.checkBox_manualMount
    update_cell(action, stepsize, table, row, col, manualCheckBox)

def x_down(gui):
    row = [0]
    col = 0
    action = "down"
    stepsize = gui.text_mountStepSize_um
    table = gui.table_mountPos_xyz
    manualCheckBox = gui.checkBox_manualMount
    update_cell(action, stepsize, table, row, col, manualCheckBox)

def y_up(gui):
    row = [0]
    col = 1
    action = "up"
    stepsize = gui.text_mountStepSize_um
    table = gui.table_mountPos_xyz
    manualCheckBox = gui.checkBox_manualMount
    update_cell(action, stepsize, table, row, col, manualCheckBox)

def y_down(gui):
    row = [0]
    col = 1
    action = "down"
    stepsize = gui.text_mountStepSize_um
    table = gui.table_mountPos_xyz
    manualCheckBox = gui.checkBox_manualMount
    update_cell(action, stepsize, table, row, col, manualCheckBox)

def z_up(gui):
    row = [0]
    col = 2
    action = "up"
    stepsize = gui.text_mountStepSize_um
    table = gui.table_mountPos_xyz
    manualCheckBox = gui.checkBox_manualMount
    update_cell(action, stepsize, table, row, col, manualCheckBox)

def z_down(gui):
    row = [0]
    col = 2
    action = "down"
    stepsize = gui.text_mountStepSize_um
    table = gui.table_mountPos_xyz
    manualCheckBox = gui.checkBox_manualMount
    update_cell(action, stepsize, table, row, col, manualCheckBox)


def roll_up(gui):
    row = [0]
    col = 0
    action = "up"
    stepsize = gui.text_mountStepSize_urad
    table = gui.table_mountPos_rpy
    manualCheckBox = gui.checkBox_manualMount
    update_cell(action, stepsize, table, row, col, manualCheckBox)


def roll_down(gui):
    # if gui.checkBox_manualMount.isChecked():
    row = [0]
    col = 0
    action = "down"
    stepsize = gui.text_mountStepSize_urad
    table = gui.table_mountPos_rpy
    manualCheckBox = gui.checkBox_manualMount
    update_cell(action, stepsize, table, row, col, manualCheckBox)


def pitch_up(gui):
    # if gui.checkBox_manualMount.isChecked():
    row = [0]
    col = 1
    action = "up"
    stepsize = gui.text_mountStepSize_urad
    table = gui.table_mountPos_rpy
    manualCheckBox = gui.checkBox_manualMount
    update_cell(action, stepsize, table, row, col, manualCheckBox)


def pitch_down(gui):
    # if gui.checkBox_manualMount.isChecked():
    row = [0]
    col = 1
    action = "down"
    stepsize = gui.text_mountStepSize_urad
    table = gui.table_mountPos_rpy
    manualCheckBox = gui.checkBox_manualMount
    update_cell(action, stepsize, table, row, col, manualCheckBox)


def yaw_up(gui):
    # if gui.checkBox_manualMount.isChecked():
    row = [0]
    col = 2
    action = "up"
    stepsize = gui.text_mountStepSize_urad
    table = gui.table_mountPos_rpy
    manualCheckBox = gui.checkBox_manualMount
    update_cell(action, stepsize, table, row, col, manualCheckBox)


def yaw_down(gui):

    row = [0]
    col = 2
    action = "down"
    stepsize = gui.text_mountStepSize_urad
    table = gui.table_mountPos_rpy
    manualCheckBox = gui.checkBox_manualMount
    update_cell(action, stepsize, table, row, col, manualCheckBox)


def update_cell(action, stepsize, table, row, col, manualCheckBox):

    step = stepsize.text()

    if not manualCheckBox.isChecked():
        print("Manual control not enabled.")
        return


    if step is not None and manualCheckBox.isChecked():
        try:
            step_value = float(step)

            for r in row:
                # Check if the cell value to be changed is even a float
                try:
                    item = table.item(r, col)

                    if item is None:  # If nothing is in the cell
                        emptycell_value = 0.000
                        item = QtWidgets.QTableWidgetItem(f"{emptycell_value}")

                    cell_value = float(item.text())

                    if action == "down":
                        new_cell_value = cell_value - step_value
                    elif action == "up":
                        new_cell_value = cell_value + step_value
                    else:
                        print("Invalid action.")
                        new_cell_value = cell_value

                    new_item = QtWidgets.QTableWidgetItem("{:.3f}".format(new_cell_value))


                    table.setItem(r, col, new_item)

                except ValueError:
                    print("Cell value is not a float.")
        except ValueError:
            print("Step value is not a float.")
    else:
        print("No step size given.")