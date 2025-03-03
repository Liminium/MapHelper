import random
import sys

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import uic

import icons
from settings import *


class EasterEggDialog(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("easter_egg.ui", self)

        self.time_to_close = 60 * 3 + 14
        self.close_clicks = 0
        self.current_stage = 1
        self.times_trolled = 0

        self.ok_btn_prev_x = -1

        self.amount_of_clicks = None
        self.amount_is_chosen = False
        self.times_chosen = 0

        self.close_messages = ["Are you surely sure?", "Some things can happen once...", "Some time it will be just closed.",
                               "Are you giving up?", "Do you always give up so quickly?",
                               "Even a jellyfish can solve this task.", "Terminating was not started.",
                               "Why are you clicking this cross?"]

        self.wrong_answer_messages = ["Are you serious?", "Think harder.", "My hedgehog answered it correctly...",
                                      "That's the easiest question...", "Think better... Or just think."]

        self.ok_button_functions = ["ok_function_first_stage", "ok_function_second_stage"]

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.vanish_message_timer = QTimer()
        self.vanish_message_timer.timeout.connect(self.vanish_message)

        self.time_timer = QTimer()
        self.time_timer.timeout.connect(self.change_time)
        self.time_timer.start(1000)

        self.message_timer = QTimer()

        self.choose_digit_timer = QTimer()
        self.choose_digit_timer.timeout.connect(self.choose_digit)

        self.close_btn.clicked.connect(self.close_function)
        self.ok_btn.clicked.connect(self.ok_function_first_stage)
        self.test_luck_btn.clicked.connect(self.test_luck)

        self.shadow = QGraphicsDropShadowEffect(self.frame)
        self.shadow.setBlurRadius(16)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 200))
        self.setGraphicsEffect(self.shadow)

        self.stage_frame.setCurrentIndex(0)
        for widget in (self.hundred_digit, self.ten_digit, self.one_digit):
            widget.hide()
            widget.setEnabled(False)
        self.test_luck_btn.hide()

    def test_luck(self):
        self.hundred_digit.show()
        self.ten_digit.show()
        self.one_digit.show()
        self.sender().hide()
        self.choose_digit_timer.start(200)

    def choose_digit(self):

        a, b, c = str(random.randint(1, 9)), str(random.randint(0, 9)), str(random.randint(1, 9))

        for (widget, text) in zip((self.hundred_digit, self.ten_digit, self.one_digit), (a, b, c)):
            widget.setText(text)

        self.times_chosen += 1

        if self.times_chosen == 20:

            self.choose_digit_timer.stop()
            self.ok_btn.show()
            self.amount_of_clicks = int(f"{a}{b}{c}")
            self.amount_is_chosen = True
            self.start_writing(f"That is your goal!\nGood luck.")

            for widget in (self.hundred_digit, self.ten_digit, self.one_digit):
                widget.setStyleSheet(INACTIVE_DIGIT_STYLE)

    def close_function(self):
        self.close_clicks += 1

        if self.close_clicks == 1:
            self.start_writing("Are you sure?\nThis secret window can be opened once.",)
        elif self.close_clicks in (2, 3):
            self.start_writing(self.close_messages.pop(random.randrange(0, len(self.close_messages))))
        else:
            self.close()

    def ok_function_first_stage(self):
        data = self.input_lineedit.text()
        if data.lower() == 'pi':
            self.start_next_stage()
            self.set_second_stage()
            self.start_writing("That's right. Congratulations.\n*loud applause sounds*")
        else:
            if data:
                self.start_writing(self.wrong_answer_messages[random.randrange(0, len(self.wrong_answer_messages))])

    def ok_function_second_stage(self):
        pass

    def set_second_stage(self):
        self.ok_btn.disconnect()
        self.time_timer.stop()
        self.ok_btn.setEnabled(False)
        self.ok_btn.installEventFilter(self)
        self.title.setText(f"Times trolled: {self.times_trolled}")

    def start_next_stage(self):
        self.current_stage += 1
        self.stage_frame.setCurrentIndex(self.current_stage - 1)
        self.ok_btn.disconnect()
        self.ok_btn.clicked.connect(getattr(self, self.ok_button_functions[self.current_stage - 1]))

    def start_writing(self, message: str):
        try:
            self.message_timer.disconnect()  # In case of being disconnected in advance
        except TypeError:
            pass
        getattr(self, f"message_{self.current_stage}_label").setText("")

        self.message_timer.timeout.connect(lambda: self.write_message(message))
        self.message_timer.start(150)

    def change_time(self) -> None:
        self.title.setText(f"Time left:  {self.time_to_close // 60}:{str(self.time_to_close % 60).rjust(2, '0')}")
        self.time_to_close -= 1
        if self.time_to_close == 2:
            self.start_writing("Time's up!")
        if self.time_to_close == -1:
            self.time_timer.stop()
            self.close()

    def vanish_message(self) -> None:
        getattr(self, f"message_{self.current_stage}_label").setText('')
        self.vanish_message_timer.stop()

    def write_message(self, message) -> None:
        """Writes the message"""
        phrase = f'{message}'
        getattr(self, f"message_{self.current_stage}_label").setText(phrase[0:len(getattr(self, f"message_{self.current_stage}_label").text()) + 1])

        if getattr(self, f"message_{self.current_stage}_label").text() == phrase:
            self.vanish_message_timer.start(1000)
            self.message_timer.stop()

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Enter:

            # Avoid a mouse being on a new generated button
            new_x = random.randint(9, self.frame_3.width() - self.ok_btn.width() - 9)
            while self.has_intersection(new_x, self.ok_btn_prev_x, self.ok_btn.width()):
                new_x = random.randint(9, self.frame_3.width() - self.ok_btn.width() - 9)
            self.ok_btn.move(new_x, 9)
            self.ok_btn_prev_x = new_x

            self.times_trolled += 1
            self.title.setText(f"Times trolled: {self.times_trolled}")

            if self.times_trolled == 50:  # 50
                self.start_writing("It's going to take a lot of time...")

            if self.times_trolled == 75:
                self.start_writing("Let's play a game of your luck...")

            if self.times_trolled == 90:
                self.start_writing("...and find out how many times\nyou have to be trolled!")

            if self.times_trolled == 100:
                self.test_luck_btn.show()
                self.ok_btn.hide()

            if self.amount_is_chosen:
                if (not (n := (self.amount_of_clicks - self.times_trolled)) % 25) and \
                        (self.amount_of_clicks != self.times_trolled):
                    self.start_writing(f"Times left: {n}.")
                if self.amount_of_clicks == self.times_trolled:
                    self.start_writing(f"You are a true hard-worker...")
        return False

    @staticmethod
    def has_intersection(x1, x2, width):
        return (x1 <= x2 <= x1 + width) or (x2 <= x1 <= x2 + width)