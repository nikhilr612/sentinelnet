"""
Define a subclass of the MainWindow class exposed by ui_mainwin_def, so that
the generated file may be replaced without requiring re-writes or frequent re-factoring.
"""

from ui_mainwin_def import Ui_MainWindow
from PySide6 import QtWidgets
import sys
import os

class MainWindowImpl(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__();
        self.setupUi(self);
        # Initialize widgets here, and bind callbacks.

    @staticmethod
    def show_ui():
        qt_app = QtWidgets.QApplication(sys.argv);
        if os.path.exists("./style.qss"):
            with open("./style.qss") as f:
                qt_app.setStyleSheet(f.read())
        app = MainWindowImpl();
        app.show();
        qt_app.exec();

if __name__ == "__main__":
    MainWindowImpl.show_ui()
