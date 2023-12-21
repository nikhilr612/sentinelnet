"""
Define a subclass of the MainWindow class exposed by ui_mainwin_def, so that
the generated file may be replaced without requiring re-writes or frequent re-factoring.
"""

from ui.ui_mainwin_def import Ui_MainWindow
from ui.ui_nodelist_def import Ui_NodeListDialog
from PySide6 import QtWidgets, QtCore
import sys
import os
from server_launch import r as redis_conn
from server_launch import PREFIX

NODE_LIST_CAP = 128;

class EmittingStream(QtCore.QObject):
    textWritten = QtCore.Signal(str)
    def write(self, text):
        self.textWritten.emit(str(text))

class ListDialogImpl(QtWidgets.QDialog, Ui_NodeListDialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self);
        display_list = [];
        for i, key in enumerate(redis_conn.scan_iter(PREFIX+":")):
            if i >= NODE_LIST_CAP:
                break;
            else:
                display_list.append(key);
        self.listWidget.addItems(display_list);
        

class MainWindowImpl(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.offender_list.clear();
        self.offender_list.itemDoubleClicked.connect(self._switch_view);
        self.current_view = None;
        sys.stdout = EmittingStream();
        sys.stdout.textWritten.connect(self.plainTextEdit.appendPlainText);
        self.action_ListNodes.triggered.connect(self._spawn_dialog);
        # Initialize widgets here, and bind callbacks.

    def _spawn_dialog(self):
        ldiag = ListDialogImpl();
        ldiag.show();

    def _switch_view(self, selected_item):
        self.current_view = selected_item;
        print("Changing to: ", selected_item)

    @staticmethod
    def show_ui():
        qt_app = QtWidgets.QApplication(sys.argv)
        if os.path.exists("./style.qss"):
            with open("./style.qss") as f:
                qt_app.setStyleSheet(f.read())
        app = MainWindowImpl()
        app.show()
        return (qt_app, app)


if __name__ == "__main__":
    qt_app, app = MainWindowImpl.show_ui()
    qt_app.exec();
