'''
This is the root of the branch for the GUI. It is the main file that should be run to start the GUI.
'''

# Import statements
import sys
from main_window import Ui_MainWindow
from PyQt5 import QtWidgets


def finalFunction_mems(mems):
    mems.closeDM()
    print('DM closed successfully')

def finalFunction_mount(mount):
    try:
        mount.closeFile()
        print('File closed successfully')
    except Exception as e:
        print('Error:', e)

# Create the GUI
app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)


# Open the MEMs and mount
openDevices = True
shm = True
if openDevices:
    from open_devices import devices
    mems, mount, cameras = devices()
else:
    mems = None
    mount = None
    cameras = None


try:
    # Preprocessing gui
    from preprocessing import startup
    startup(ui)


    # Control triggers
    from signals import triggers
    triggers(ui,mems,mount, cameras)


    # Run the GUI
    MainWindow.show()

    if openDevices and not shm:
        app.aboutToQuit.connect(lambda: finalFunction_mems(mems))
        app.aboutToQuit.connect(lambda: finalFunction_mount(mount))

except Exception as e:
    print('Error:', e)

    if openDevices:
        finalFunction_mems(mems)
        finalFunction_mount(mount)
    


sys.exit(app.exec_())



