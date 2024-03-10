from GUI_ui import Ui_MainWindow
from GUI_triggers import triggers, preprocessing
from PyQt5 import QtCore, QtGui, QtWidgets



import sys
app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
triggers(ui)
preprocessing(ui)
MainWindow.show()
sys.exit(app.exec_())



