import sys
import time

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic

import random

from circular_progress import CircularProgress

from settings import *


class SplashScreen(QMainWindow):

    counter = 0
    transparency_degree = 255

    def __init__(self, main_window):
        super().__init__()
        uic.loadUi("splash_interface.ui", self)

        self.another_thread = AnotherThread()
        self.another_thread.finished.connect(self.show_connection_error)

        self.data_message.setText(FAKE_INFO.pop(random.randrange(0, len(FAKE_INFO))))

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.titles_count = 1
        self.multiplier = 1

        # Creating Progress Bar
        self.progress = CircularProgress(0, width=400, height=400, progress_width=12, is_rounded=True, font_size=35,
                                         color_of_progress=(189, 147, 249),
                                         text_color=(255, 121, 198), bg_color=(99, 99, 99, 199))

        # Moving / resizing
        self.progress.move(25, 13)
        self.progress.setParent(self.centralwidget)

        self.progress.show()

        # Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(25)

        # Timer to make title invisible
        self.timer_ = QTimer()
        self.timer_.timeout.connect(self.make_transparent)
        self.timer_.start(7)

        # Timer to check if pc has Internet connection
        self.check_connection_timer = QTimer()
        self.check_connection_timer.timeout.connect(self.check_connection)
        self.check_connection_timer.start(250)

        self.main_window = main_window

    def check_connection(self) -> None:
        """Проверка подключения к интернету"""
        self.another_thread.start()
        self.check_connection_timer.stop()

    def show_connection_error(self):
        if self.another_thread.exception_class in EXCEPTIONS:
            self.generate_message('connection')

    def make_transparent(self):
        """Изменение надписей на SplashScreen"""
        if self.transparency_degree <= 0 or self.transparency_degree >= 255:
            if self.transparency_degree <= 0:
                if self.titles_count == 3:
                    self.data_message.setText(u"<strong>Done.</strong>")
                else:
                    self.data_message.setText(FAKE_INFO.pop(random.randrange(0, len(FAKE_INFO))))
                    self.titles_count += 1
            self.multiplier *= -1

        if self.data_message.text() == u"<strong>Done.</strong>" and self.transparency_degree >= 255:
            self.timer_.stop()

        self.transparency_degree += 3 * self.multiplier
        self.data_message.setStyleSheet(f"color: rgb(245, 245, 245, {self.transparency_degree})")

    def update(self):
        """Обновление шкалы ProgressBar'а"""
        # Set value to progress bar

        self.visible_counter = self.counter

        # Wait some seconds after timer reaches 100
        if self.counter > 100:
            self.visible_counter = 100

        self.progress.set_value(self.visible_counter)

        # Close welcome screen and open main app
        if self.counter > 125:
            # Stop timer
            self.timer.stop()

            # Show main window
            self.window_ = self.main_window()
            self.window_.show(is_being_opened=True)

            # Close splash screen
            self.close()

        self.counter += 1
