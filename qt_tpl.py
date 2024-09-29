import sys
from PyQt6 import QtWidgets as qtw
from PyQt6 import QtGui as qtg
from PyQt6 import QtCore as qtc


class MainWindow(qtw.QWidget):

    def __init__(self):
        """MainWindow Constructor"""
        super().__init__()
        # main ui code goes here

        # end main ui code
        self.show()


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec())