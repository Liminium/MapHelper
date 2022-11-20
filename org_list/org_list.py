import sys
import webbrowser

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import uic


class OrganisationList(QDialog):
    def __init__(self, organisations):
        super().__init__()
        uic.loadUi('org_list/org_list.ui', self)

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.title.mouseMoveEvent = self.move_window

        self.close_window_system.clicked.connect(self.close)

        for org in organisations:
            gen = ("Not found" if i is None else i[:25] + "..." for i in (org.id, org.name, org.address, org.coordinates, org.categories, org.hours, org.phone, org.website, org.rating))
            self.generate_frame(*gen)

    def generate_frame(self, id, name, address, coordinates, categories, hours, phone, web_site, rating):
        categories = ','.join(set(categories.split(', '))).capitalize()
        self.org_frame = QFrame(self.scrollAreaWidgetContents)
        self.verticalLayout_3.addWidget(self.org_frame)
        self.org_frame.setObjectName(u"org_frame")
        self.org_frame.setGeometry(QRect(132, 212, 505, 250))
        self.org_frame.setMinimumSize(QSize(0, 250))
        self.org_frame.setMaximumSize(QSize(16777215, 250))
        font = QFont()
        font.setPointSize(10)
        self.org_frame.setFont(font)
        self.org_frame.setStyleSheet(u"QFrame {background-color: rgb(47, 48, 62);\n"
                                     "border-radius: 10px;\n"
                                     "border-top-right-radius: 0px;\n"
                                     "border-top-left-radius: 0px;\n"
                                     "border-top: 2px solid rgb(189, 147, 249)}\n"
                                     "\n"
                                     "QFrame:hover {\n"
                                     "	background-color: rgb(50, 50, 67);\n"
                                     "}")
        self.org_frame.setFrameShape(QFrame.StyledPanel)
        self.org_frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.org_frame)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.frame_3 = QFrame(self.org_frame)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMinimumSize(QSize(340, 0))
        self.frame_3.setMaximumSize(QSize(16777215, 16777215))
        self.frame_3.setStyleSheet(u"background-color: transparent;\n"
                                   "border: none")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.frame_3.setMaximumSize(340, 248)
        self.verticalLayout_4 = QVBoxLayout(self.frame_3)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        name_btn = QPushButton(self.frame_3)
        name_btn.setObjectName(u"name_btn")
        name_btn.setMaximumSize(QSize(16777215, 22))
        name_btn.setText(f"Name: {name}")
        font1 = QFont()

        font1.setFamily(u"Open Sans")
        font1.setPointSize(10)
        name_btn.setFont(font1)
        name_btn.setCursor(QCursor(Qt.PointingHandCursor))
        name_btn.setStyleSheet(
            u"QPushButton {color: rgb(177, 185, 194, 255); text-align: left; padding-left: 15px;}\n"
            "\n"
            "QPushButton:pressed {color: rgb(210, 220, 230)}")

        self.verticalLayout_4.addWidget(name_btn)

        address_btn = QPushButton(self.frame_3)
        address_btn.setObjectName(u"address__btn")
        address_btn.setMaximumSize(QSize(16777215, 22))
        address_btn.setFont(font1)
        address_btn.setCursor(QCursor(Qt.PointingHandCursor))
        address_btn.setText(f"Address: {address}")
        address_btn.setStyleSheet(
            u"QPushButton {color: rgb(177, 185, 194, 255); text-align: left; padding-left: 15px;}\n"
            "\n"
            "QPushButton:pressed {color: rgb(210, 220, 230)}")

        self.verticalLayout_4.addWidget(address_btn)

        coordinates_btn = QPushButton(self.frame_3)
        coordinates_btn.setObjectName(u"coordinates_btn")
        coordinates_btn.setMaximumSize(QSize(16777215, 22))
        coordinates_btn.setFont(font1)
        coordinates_btn.setCursor(QCursor(Qt.PointingHandCursor))
        coordinates_btn.setStyleSheet(
            u"QPushButton {color: rgb(177, 185, 194, 255); text-align: left; padding-left: 15px;}\n"
            "\n"
            "QPushButton:pressed {color: rgb(210, 220, 230)}")
        coordinates_btn.setText(f"Coordinates: {coordinates}")
        self.verticalLayout_4.addWidget(coordinates_btn)

        categories_btn = QPushButton(self.frame_3)
        categories_btn.setObjectName(u"categories_btn")
        categories_btn.setMaximumSize(QSize(16777215, 22))
        categories_btn.setFont(font1)
        categories_btn.setText(f"Categories: {categories}")
        categories_btn.setCursor(QCursor(Qt.PointingHandCursor))
        categories_btn.setStyleSheet(
            u"QPushButton {color: rgb(177, 185, 194, 255); text-align: left; padding-left: 15px;}\n"
            "\n"
            "QPushButton:pressed {color: rgb(210, 220, 230)}")

        self.verticalLayout_4.addWidget(categories_btn)

        hours_btn = QPushButton(self.frame_3)
        hours_btn.setObjectName(u"hours_btn")
        hours_btn.setMaximumSize(QSize(16777215, 22))
        hours_btn.setFont(font1)
        hours_btn.setText(f"Working hours: {hours}")
        hours_btn.setCursor(QCursor(Qt.PointingHandCursor))
        hours_btn.setStyleSheet(
            u"QPushButton {color: rgb(177, 185, 194, 255); text-align: left; padding-left: 15px;}\n"
            "\n"
            "QPushButton:pressed {color: rgb(210, 220, 230)}")

        self.verticalLayout_4.addWidget(hours_btn)

        number_btn = QPushButton(self.frame_3)
        number_btn.setObjectName(u"number_btn")
        number_btn.setMaximumSize(QSize(16777215, 22))
        number_btn.setFont(font1)
        number_btn.setCursor(QCursor(Qt.PointingHandCursor))
        number_btn.setText(f"Phone number: {phone}")
        number_btn.setStyleSheet(
            u"QPushButton {color: rgb(177, 185, 194, 255); text-align: left; padding-left: 15px;}\n"
            "\n"
            "QPushButton:pressed {color: rgb(210, 220, 230)}")

        self.verticalLayout_4.addWidget(number_btn)

        site_btn = QPushButton(self.frame_3)
        site_btn.setObjectName(u"site_btn")
        site_btn.setMaximumSize(QSize(16777215, 22))
        site_btn.setFont(font1)
        site_btn.setText(f"Web-site: {web_site}")
        site_btn.setCursor(QCursor(Qt.PointingHandCursor))
        site_btn.setStyleSheet(
            u"QPushButton {color: rgb(177, 185, 194, 255); text-align: left; padding-left: 15px;}\n"
            "\n"
            "QPushButton:pressed {color: rgb(210, 220, 230)}")

        self.verticalLayout_4.addWidget(site_btn)

        self.horizontalLayout.addWidget(self.frame_3)

        self.label_2 = QLabel(self.org_frame)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMaximumSize(QSize(1, 200))
        self.label_2.setStyleSheet(u"border: none;\n"
                                   "background-color: rgb(143, 143, 200, 150)")

        self.horizontalLayout.addWidget(self.label_2)

        self.frame_4 = QFrame(self.org_frame)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setMaximumSize(QSize(175, 16777215))
        self.frame_4.setStyleSheet(u"background-color: transparent;\n"
                                   "border: none")
        self.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.frame_4)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.frame_6 = QFrame(self.frame_4)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setFrameShape(QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.frame_6)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        star_image = QPushButton(self.frame_6)
        star_image.setObjectName(u"star_image")
        star_image.setIconSize(QSize(120, 120))

        icon1 = QIcon()
        icon1.addFile(f":/images/icons/{round(float(rating.rstrip('...')))}_.png", QSize(), QIcon.Normal, QIcon.Off)
        star_image.setIcon(icon1)

        self.verticalLayout_5.addWidget(star_image)

        self.rating_label = QLabel(self.frame_6)
        self.rating_label.setObjectName(u"rating_label")
        self.rating_label.setText(rating.rstrip('...'))
        font2 = QFont()
        font2.setFamily(u"Open Sans")
        font2.setPointSize(15)
        self.rating_label.setFont(font2)
        self.rating_label.setStyleSheet(u"color: rgb(177, 185, 194, 255)")
        self.rating_label.setAlignment(Qt.AlignCenter)

        self.verticalLayout_5.addWidget(self.rating_label)

        self.verticalLayout_6.addWidget(self.frame_6)

        self.frame_7 = QFrame(self.frame_4)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setMinimumSize(QSize(0, 50))
        self.frame_7.setMaximumSize(QSize(16777215, 50))
        self.frame_7.setFrameShape(QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_7)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.search_btn = QPushButton(self.frame_7)
        self.search_btn.setObjectName(u"search_btn")
        self.search_btn.setMinimumSize(QSize(0, 33))
        self.search_btn.setMaximumSize(QSize(139, 32))
        self.search_btn.setText(" Search")
        self.search_btn.clicked.connect(lambda: webbrowser.open(f'https://yandex.ru/maps/org/{id}/reviews/'))
        font3 = QFont()
        font3.setFamily(u"Open Sans")
        font3.setPointSize(11)
        font3.setBold(False)
        font3.setWeight(50)
        self.search_btn.setFont(font3)
        self.search_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.search_btn.setStyleSheet(u"QPushButton {\n"
                                      "	color: rgb(255, 255, 255);\n"
                                      "	border-radius: 16px;\n"
                                      "	background-color: rgb(189, 147, 249);\n"
                                      "	padding-bottom: 1px;\n"
                                      "}\n"
                                      "\n"
                                      "QPushButton:hover {\n"
                                      "	background-color: rgba(151, 123, 200)\n"
                                      "}\n"
                                      "\n"
                                      "QPushButton:pressed {\n"
                                      "	background-color: rgb(120, 75, 186)\n"
                                      "}")
        icon = QIcon()
        icon.addFile(u":/images/icons/search.png", QSize(), QIcon.Normal, QIcon.Off)
        self.search_btn.setIcon(icon)
        self.search_btn.setIconSize(QSize(18, 18))

        self.horizontalLayout_2.addWidget(self.search_btn)

        self.verticalLayout_6.addWidget(self.frame_7)

        self.horizontalLayout.addWidget(self.frame_4)

    def move_window(self, event) -> None:
        """Function making window able to be moved"""
        if "drag_position" in self.__dict__:
            if event.buttons() == Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.drag_position)
                self.drag_position = event.globalPos()
                event.accept()

    def mousePressEvent(self, event) -> None:
        """Event activating when a mouse button getting pressed"""
        self.drag_position = event.globalPos()


if __name__ == '__main__':
    application = QApplication(sys.argv)
    window = OrganisationList()
    window.show()
    sys.exit(application.exec())
