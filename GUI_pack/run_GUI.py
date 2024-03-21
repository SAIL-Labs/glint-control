from GUI_ui import Ui_MainWindow
# from control_buttons_ui import Ui_MainWindow
from GUI_triggers import triggers, preprocessing
from PyQt5 import QtCore, QtGui, QtWidgets
from qt_material import apply_stylesheet


import sys

app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
triggers(ui)
preprocessing(ui)

MainWindow.show()
sys.exit(app.exec_())










# mems = MEMS('32AW038#027')
# mems.openDM()



# extra = {
    
#     # Density Scale
#     'density_scale': '-2',
# }
# apply_stylesheet(app, theme='dark_teal.xml', extra = extra)

