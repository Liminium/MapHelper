from core import *


class AnotherThread(QThread):
    """Класс, проверяющий в другом потоке, подключен ли пк к интернету"""

    exception_class = None

    def run(self):
        try:
            requests.get(f"https://python.org", timeout=0.5)
        except Exception as e:
            self.exception_class = type(e).__name__
        else:
            self.exception_class = False
        finally:
            return


# Decorators

def connecting_get(alt_func):
    """alt_func is a function called when ConnectionError raises"""
    def inner(func):
        """Main function"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            """Avoid raising ConnectionError"""
            try:
                return func(*args, **kwargs)
            except (requests_ReadTimeout, requests_ConnectionError):
                alt_func()

        return wrapper

    return inner


# Main data
GEOCODE_APIKEY = "40d1649f-0493-4b70-98ba-98533de7710b"
CODING = "UTF-8"

# Collections
FAKE_INFO = [u"<strong>Collecting</strong> information...", u"<strong>Analyzing </strong> resources...",
             u"<strong>Loading</strong> session...", u"<strong>Checking</strong> updates...",
             u"<strong>Processing</strong> algorithms...", u"<strong>Connecting</strong> to server...",
             u"<strong>Connecting</strong> API...", u"<strong>Updating</strong> data..."]
EXCEPTIONS = ("ConnectionError", "Timeout")
LOG_FILE_EXTENSIONS = (".txt", ".log", ".csv")
MAP_SCALES = (0.0001171875, 0.000234375, 0.00046875, 0.0009375, 0.001875, 0.00375, .0075, .015, .03, .06, .12, .24, .48,
              .96, 1.92, 3.84, 7.68, 15.36, 30.72)
TIMES_HERE = (1, 2, 3, 5, 10, 15, 25, 50, 75, 100, *(i for i in range(125, 1001, 25)))
PERCENT_DESCRIPTIONS = ("Great", "Very low", "Low", "Cooler", 'Cool', "Medium",
                        'Hot', 'Hotter', "Acceptable", "Alarming", "Extreme")
MAIN_LOGGING_FORMAT = ("app_name", "computer_user", "computer_name", "date", "time",
                       "session_id", "msg_lvl", "msg_name") + ("message",)
LOG_TYPE_TO_NUMBER = {"info": 1, "warning": 2, "error": 3}
LOG_TYPE_TO_NAME = {"info": "INFORMATION", "warning": "WARNING", "error": "ERROR"}

# Symbols
RUSSIAN_LETTERS = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
WINDOWS_FORBIDDEN_SYMBOLS = chr(34) + r"<|?*>"

# Easter eggs
SUPER_HOT_EASTER_EGG = "SUPER HOT"  # Occurs if user writes "SUPER HOT" in the log-file field
ONESTOPMID = "onestop.mid"  # Occurs when the address lineedit equals to this string

# Files
FILE_IMAGE_NAME = "image_map.png"

USER_JSON_DATA = "data/user_json_data.json"
APP_STATE_DATA = "data/app_state.json"

INFORMATION_SOUND = 'sounds/info.wav'
OPEN_SOUND = 'sounds/open.wav'
ERROR_SOUND = 'sounds/error.wav'
ACHIEVEMENT_SOUND = 'sounds/achievement.wav'
WARNING_SOUND = 'sounds/warning.wav'
ONESTOP_SOUND = 'sounds/onestop.mp3'

APP_ICON = r"icons\colorful_logo.png"
SHOW_APP_ICON = r"icons\view.png"
HIDE_APP_ICON = r"icons\hide.png"
EXIT_APP_ICON = r"icons\exit.png"

# Links
PYTHON_LINK = "https://www.python.org"
SQL_LINK = "https://sqlitestudio.pl"
QT_LINK = "https://www.qt.io"

# Default values for widgets
LOG_INFO_MESSAGE_TYPE = True
LOG_WARNING_MESSAGE_TYPE = True
LOG_ERROR_MESSAGE_TYPE = True

LOG_APP_NAME = True
LOG_COMP_USER = False
LOG_COMP_NAME = False
LOG_DATE = True
LOG_TIME = True
LOG_SESSION_ID = False
LOG_MSG_LVL = False
LOG_MSG_NAME = False
LOG_MESSAGE = True

# QSS-Styles
BLOCKING_LABEL_STYLE = "border-radius: 13px; background-color: rgb(255, 255, 255, {alpha})"
WARNING_ICON = 'image: url("icons/warning.png");'
PADDING_STYLE_SHEET = '''QPushButton {{
    color: rgb(210, 210, 210);
    border-radius: 6px;
    padding-bottom: 2px;
    background-color: none;
    text-align: left;
    padding-left: {padding}px;

}}

QPushButton:hover {{
    padding-left: {padding}px;
    background-color: rgb(255, 255, 255, 15);
}}

QPushButton:focus {{
    padding-left: {padding}px;
    background-color: rgb(255, 255, 255, 21);
    color: rgb(235, 235, 235, 255);
}}'''
ERROR_LINEEDIT_STYLE = '''QLineEdit {
                            padding-left: 10px;
                            border-radius: 17px;
                            border-top-right-radius: 0px;
                            border-bottom-right-radius: 0px;
                            background-color: rgb(255, 0, 0, 17);
                            color: rgb(200, 200, 200);
                            padding-bottom: 1px;
                            selection-background-color: rgb(247, 247, 247, 75);
                            selection-color: rgb(195, 195, 195);
                            border: 2px solid rgb(110, 15, 15);
                            border-right: transparent
                        }

                        QLineEdit:hover {
                            border-right: transparent;	
                            border: 2px solid rgb(120, 15, 15);
                            background-color: rgb(255, 0, 0, 35);
                        }

                        QLineEdit:focus {
                            border: 2px solid rgb(130, 15, 15);
                            background-color: rgb(255, 0, 0, 45);
                            border-right: transparent;
                        }'''
ORDINARY_LINEEDIT_STYLE = '''QLineEdit {
                                padding-left: 10px;
                                border-radius: 17px;
                                border-top-right-radius: 0px;
                                border-bottom-right-radius: 0px;
                                background-color: rgb(27, 29, 35);
                                selection-background-color: rgb(189, 147, 249, 150);
                                selection-color: rgb(195, 195, 195);
                                color: rgb(200, 200, 200);
                                padding-bottom: 1px;
                                border: 2px solid rgb(27, 29, 35);
                            }

                            QLineEdit:hover {
                                border: 2px solid rgb(42, 45, 54);
                                border-right: transparent;
                                background-color: rgb(34, 36, 42);
                            }

                            QLineEdit:focus {
                                background-color: rgb(34, 36, 42);
                                border: 2px solid rgb(130, 90, 207);
                                border-right: transparent
                            }
                                '''
WARNING_TITLE_STYLE = """QLabel {
                             background-color: transparent;
                             text-align: left;
                             padding-left: 10px;
                             padding-bottom: 6px;
                             padding-right: 10px;
                             color: rgb(240, 250, 141)
                         }"""
ERROR_TITLE_STYLE = """QLabel {
                           background-color: transparent;
                           text-align: left;
                           padding-left: 10px;
                           padding-bottom: 6px;		
                           padding-right: 10px;
                           color: rgb(254, 0, 0)
                        }"""
BUTTON_STYLE = """QPushButton {{
                    background-image: {image};
                    background-color: none;
                    background-position: left center;
                    background-repeat: no-repeat;
                    border-radius: 0px; 
                    color: rgb(248, 248, 244, 255);
                    border-left: 21px solid transparent;
                    padding-left: 50px;
                    text-align: left;
                    padding-bottom: 3px;
                }}
                
                QPushButton:hover {{
                    background-color: rgb(225, 225, 225, 15)
                }}
                
                QPushButton:pressed {{
                    background-color: rgb(189, 147, 249, 40)
                }}
                
                QToolTip {{	
                    border-radius: 0px;
                    background-clip: border;
                    color: rgb(180, 180, 195);
                    background-color: rgb(36, 39, 47);
                    border: 1px solid rgb(40, 45, 70);
                    border-left: 2px solid rgb(174, 136, 230);
                    text-align: left;
                    padding-left: 1px
                }}"""
FOCUSED_BUTTON_STYLE = """QPushButton {{
                            background-image: {image};
                            background-color: none;
                            background-position: left center;
                            background-repeat: no-repeat;
                            border-radius: 0px; 
                            color: rgb(248, 248, 244, 255);
                            border-left: 21px solid transparent;
                            padding-left: 50px;
                            text-align: left;
                            border-right: 2px solid rgb(189, 147, 249); 
                            background-color: rgba(189, 147, 249, 40);
                            padding-bottom: 3px;
                        }}
                        
                        QToolTip {{	
                            border-radius: 0px;
                            background-clip: border;
                            color: rgb(180, 180, 195);
                            background-color: rgb(36, 39, 47);
                            border: 1px solid rgb(40, 45, 70);
                            border-left: 2px solid rgb(174, 136, 230);
                            text-align: left;
                            padding-left: 1px
                        }}"""
ANDROID_LABEL_STYLE = """background-color: rgba(77, 77, 77, {alpha});
                         color: rgb(255, 255, 255, {alpha});
                         padding-bottom: 2px;
                         border-radius: 12px;"""
ORDINARY_CHOICE_BUTTON_STYLE = """QPushButton {
                                      color: rgb(198, 207, 217);
                                      text-align: left;
                                      padding-left: 20px;
                                      background-color: rgb(27, 29, 35);
	border-radius: 4px;
	padding-bottom: 4px
}

QPushButton:hover {
	background-color: rgb(37, 41, 50)
}

QPushButton:pressed {
	background-color: rgb(46, 49, 59); 
	color: rgb(250, 250, 250)
}"""
SELECTED_CHOICE_BUTTON_STYLE = """QPushButton {
                                      color: rgb(250, 250, 250);
                                      text-align: left;
                                      padding-left: 20px;
                                      background-color: rgb(46, 49, 59);
	border-radius: 4px;
	padding-bottom: 4px}
QPushButton:hover {background-color: rgb(50, 54, 63)}
"""
TRAY_MENU_STYLE = """QMenu { 
                            background-color: rgb(34, 34, 45) 
                           } 
                     QMenu::item { 
                            color: rgb(175, 175, 190) 
                           } 
                     QMenu::item:selected { 
                            color: rgb(189, 147, 249); 
                            background-color: rgb(45, 45, 54)
                           }"""
INACTIVE_DIGIT_STYLE = '''QLineEdit {
padding-left: 2px;
border-radius: 10px;
background-color: rgb(27, 29, 35);
color: rgb(200, 200, 200);
padding-bottom: 4px;
border: 2px solid rgb(27, 29, 35);
}

QLineEdit:focus{
background-color: rgb(34, 36, 42);
border: 2px solid rgb(130, 90, 207);
}'''

ACTIVE_DIGIT_STYLE = """
QLineEdit {
padding-left: 2px;
border-radius: 10px;
color: rgb(200, 200, 200);
padding-bottom: 4px;
background-color: rgb(34, 36, 42);
border: 2px solid rgb(130, 90, 207);
}"""