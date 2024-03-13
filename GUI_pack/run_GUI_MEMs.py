# from GUI_ui import Ui_MainWindow
# import sys
# sys.path.append('/home/scexao/steph/control-code')

# import apiMEMsControl 
# import chipMountControl 

from control_buttons_ui import Ui_MainWindow
from GUI_triggers_MEMs import triggers, preprocessing
from PyQt5 import QtCore, QtGui, QtWidgets
from qt_material import apply_stylesheet

import sys

# def finalFunction(mems):
#     mems.closeDM()
#     print('DM closed successfully')

# mems = apiMEMsControl.MEMS('32AW038#027')
# mems.openDM()
# print('DM opened successfully')

# mount = chipMountControl.Mount('/dev/serial/by-id/usb-SURUGA_SEIKI_SURUGA_SEIKI_DS102-if00-port0', 38400)
# print(mount.idn())

app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)

try:
    triggers(ui)
    # triggers(ui, mems, mount)
    # preprocessing(ui)

    MainWindow.show()

    # app.aboutToQuit.connect(lambda: finalFunction(mems))

    sys.exit(app.exec_())
except Exception as e:
    print(e)
    # finalFunction(mems)
    sys.exit(app.exec_())
    










# mems = MEMS('32AW038#027')
# mems.openDM()



# extra = {
    
#     # Density Scale
#     'density_scale': '-2',
# }
# apply_stylesheet(app, theme='dark_teal.xml', extra = extra)

