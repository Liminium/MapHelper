import sys

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic
import images

import webbrowser


class ErrorMessage(QDialog):
    def __init__(self, parent_window: QWidget):
        super().__init__()
        uic.loadUi("error_message.ui", self)

        self.parent_window = parent_window

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.button_close.clicked.connect(lambda: self.close())
        self.button_contact.clicked.connect(lambda: webbrowser.open("https://www.google.com"))  # TODO
        self.reconnect_button.clicked.connect(self.reconnect)

    def reconnect(self):
        self.close()
        self.parent_window.show()


if __name__ == '__main__':
    q = QApplication(sys.argv)
    dialog = ErrorMessage(QWidget())
    dialog.show()
    sys.exit(q.exec())

