# pyuic5 src\assistant.ui -o va_ui.py
from PyQt5 import QtWidgets
from gui import Ui_MainWindow
import sys


class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


app = QtWidgets.QApplication([])
application = MyWindow()
application.show()

sys.exit(app.exec())
