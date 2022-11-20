from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class CircularProgress(QWidget):
    def __init__(self, delta_h: int, /, value: int = 0, width: int = 455, height: int = 455, progress_width: int = 12,
                 is_rounded: bool = True, max_value: int = 100, font_family: str = "Segoe UI",
                 font_size: int = 12, suffix: str = "%", enable_shadow: bool = True,
                 color_of_progress: tuple[int] = (255, 255, 255),
                 text_color: tuple[int] = (255, 255, 255), bg_color: tuple[int] = (100, 100, 100)):

        super(CircularProgress, self).__init__()

        # Custom features
        self.delta_h = delta_h
        self.value = value
        self.width = width
        self.height = height
        self.progress_width = progress_width
        self.is_rounded = is_rounded
        self.color_of_progress = color_of_progress
        self.max_value = max_value
        self.font_family = font_family
        self.font_size = font_size
        self.suffix = suffix
        self.text_color = text_color
        self.bg_color = bg_color
        self.add_dropping_shadow(enable_shadow)

        # Set the default size without any layouts
        self.setFixedSize(self.width, self.height)

    def set_value(self, value) -> None:
        self.value = value
        self.repaint()  # Render progress bar changing

    def add_dropping_shadow(self, enable: bool) -> None:
        if enable:
            self.shadow = QGraphicsDropShadowEffect(self)
            self.shadow.setBlurRadius(15)
            self.shadow.setYOffset(0)
            self.shadow.setXOffset(0)
            self.shadow.setColor(QColor(0, 0, 0, 120))
            self.setGraphicsEffect(self.shadow)

    def paintEvent(self, qp: QPainter) -> None:
        width = self.width - self.progress_width
        height = self.height - self.progress_width
        margin = self.progress_width / 2
        value = self.value * 360 / self.max_value

        # Painter
        paint = QPainter()
        paint.begin(self)
        paint.setRenderHint(QPainter.Antialiasing)  # remove pixel-ages
        paint.setFont(QFont(self.font_family, self.font_size))

        # Create rectangle
        rectangle = QRect(0, 0, self.width, self.height)
        paint.setPen(Qt.NoPen)
        paint.drawRect(rectangle)

        # Pen
        pen = QPen()
        pen.setWidth(self.progress_width)
        # Set round ages (cap)
        if self.is_rounded:
            pen.setCapStyle(Qt.RoundCap)

        pen.setColor(QColor(*self.bg_color))
        paint.setPen(pen)
        paint.drawArc(margin, margin, width, height, 0, 360 * 16)

        # Create ABC / Circular progress
        pen.setColor(QColor(*self.color_of_progress))
        paint.setPen(pen)
        paint.drawArc(margin, margin, width, height, -90 * 16, -value * 16)

        # Create text
        pen.setColor(QColor(*self.text_color))
        paint.setPen(pen)

        font = QFont("Segoe Ui")
        font.setPointSize(self.font_size)
        paint.setFont(font)

        paint.drawText(QRect(0, 0, self.width, self.height + self.delta_h), Qt.AlignCenter, f"{self.value} {self.suffix}")
        # End
        paint.end()


