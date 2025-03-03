# -*- coding: utf-8 -*-

from core import *
from settings import *

import icons

from warning import WarningDialog
from time_here import TimeHereDialog
from easter_egg import EasterEggDialog
from splash_screen import SplashScreen
from toggle_button import ToggleButton
from circular_progress import CircularProgress
from logger import Logger

cr.init(autoreset=True)


KEY_BOARD_KEYS_DICTIONARY = {value: key.partition('_')[2] for (key, value) in vars(Qt).items() if isinstance(value, Qt.Key)}
MODIFIERS_DICTIONARY = {
    Qt.ControlModifier: KEY_BOARD_KEYS_DICTIONARY[Qt.Key_Control],
    Qt.AltModifier: KEY_BOARD_KEYS_DICTIONARY[Qt.Key_Alt],
    Qt.ShiftModifier: KEY_BOARD_KEYS_DICTIONARY[Qt.Key_Shift],
    Qt.MetaModifier: KEY_BOARD_KEYS_DICTIONARY[Qt.Key_Meta],
    Qt.GroupSwitchModifier: KEY_BOARD_KEYS_DICTIONARY[Qt.Key_AltGr],
    Qt.KeypadModifier: KEY_BOARD_KEYS_DICTIONARY[Qt.Key_NumLock],
    }


def keyevent_to_str(event, sep: str) -> str:
    sequence = []
    for modifier, text in MODIFIERS_DICTIONARY.items():
        if event.modifiers() & modifier:
            sequence.append(text)
    key = KEY_BOARD_KEYS_DICTIONARY.get(event.key(), event.text())
    if key not in sequence:
        sequence.append(key)
    return sep.join(sequence)


def get_json_data(filename: str) -> dict:
    """Reads the json data from a specified file"""
    with open(filename, mode='rt', encoding=CODING) as jd:
        return json.load(jd)


def write_json_data(*, filename: str, indent: int = 4, ensure_ascii: bool = False, **json_data) -> None:
    """Writes json data to the user json-data file"""
    with open(filename, mode='r', encoding=CODING) as user_jd_r:
        old_data = json.load(user_jd_r)
    with open(filename, mode='w', encoding=CODING) as user_jd_w:
        json.dump(obj=(old_data | json_data), fp=user_jd_w, indent=indent, ensure_ascii=ensure_ascii)


def except_exceptions(clas_, exception, callback):
    sys.__excepthook__(clas_, exception, callback)


class UiFunctionality:
    """The class-mixin implements UI-functionality and interacting with its widgets.
       Every custom widget created in this class must have the unique name.
       By this name the state of the current widget will be restored from .json file."""

    def toggle_left_menu(self) -> None:
        """Toggling left menu"""

        # Frame and delimiter dimensions
        min_frame_width = 67
        max_frame_width = 210

        min_delimiter_width = 53
        max_delimiter_width = 196

        start_frame_width = self.leftmenu_frame.width()
        start_label_width = self.leftmenu_delimiter.width()

        if start_frame_width == min_frame_width:
            final_label_width = max_delimiter_width
            final_frame_width = max_frame_width
        elif start_frame_width == max_frame_width:
            final_frame_width = min_frame_width
            final_label_width = min_delimiter_width
        else:
            return

        # Disable expand sidebar for all buttons except for main hamburger button
        if self.sender() != self.menu_button and start_label_width == min_delimiter_width:
            return

        # Animations
        self.frame_animation = QPropertyAnimation(self.leftmenu_frame, b"minimumWidth")
        self.frame_animation.setDuration(750)
        self.frame_animation.setStartValue(start_frame_width)
        self.frame_animation.setEndValue(final_frame_width)
        self.frame_animation.setEasingCurve(QEasingCurve.InOutCubic)

        self.split_animation = QPropertyAnimation(self.leftmenu_delimiter, b"minimumWidth")
        self.split_animation.setDuration(750)
        self.split_animation.setStartValue(start_label_width)
        self.split_animation.setEndValue(final_label_width)
        self.split_animation.setEasingCurve(QEasingCurve.InOutCubic)

        self.animation_group = QParallelAnimationGroup()
        self.animation_group.addAnimation(self.frame_animation)
        self.animation_group.addAnimation(self.split_animation)
        self.animation_group.start()

    def extend_setting_leftmenu(self) -> None:
        """Extend settings left-menu frame"""
        if self.settings_left_manu_frame.width() == 0:
            # Animations
            self.settings_shrink_animation = QPropertyAnimation(self.settings_left_manu_frame, b"maximumWidth")
            self.settings_shrink_animation.setDuration(950)
            self.settings_shrink_animation.setStartValue(self.settings_left_manu_frame.width())
            self.settings_shrink_animation.setEndValue(250)
            self.settings_shrink_animation.setEasingCurve(QEasingCurve.InOutCubic)
            self.settings_shrink_animation.start()

    def shrink_setting_leftmenu(self, event) -> None:
        """Shrink settings left menu"""
        if self.settings_left_manu_frame.width() == 250:
            # Animations
            self.setting_frame_shrink_animation = QPropertyAnimation(self.settings_left_manu_frame, b"maximumWidth")
            self.setting_frame_shrink_animation.setDuration(950)
            self.setting_frame_shrink_animation.setStartValue(self.settings_left_manu_frame.width())
            self.setting_frame_shrink_animation.setEndValue(0)
            self.setting_frame_shrink_animation.setEasingCurve(QEasingCurve.InOutCubic)
            self.setting_frame_shrink_animation.start()

    def add_shadows(self, *widgets: tuple[QWidget:],
                    shadow_color: tuple, blurring: int, x_offset: int, y_offset: int) -> None:
        """Set the shadow to all parent widget's children dependently on the specified condition"""
        for cur_widget in widgets:
            self.widget_shadow = QGraphicsDropShadowEffect(cur_widget)
            self.widget_shadow.setBlurRadius(blurring)
            self.widget_shadow.setColor(QColor(*shadow_color))
            self.widget_shadow.setXOffset(x_offset)
            self.widget_shadow.setYOffset(y_offset)
            cur_widget.setGraphicsEffect(self.widget_shadow)

    def set_display_msg_types_toggle_buttons(self) -> None:
        """Sets custom widgets on settings page in 'display message types'"""
        self.information_msg_type_tb = ToggleButton(self.frame_155)
        self.horizontalLayout_126.addWidget(self.information_msg_type_tb)
        self.information_msg_type_tb.setObjectName('information_msg_type_tb')

        self.warning_msg_type_tb = ToggleButton(self.frame_156)
        self.horizontalLayout_127.addWidget(self.warning_msg_type_tb)
        self.warning_msg_type_tb.setObjectName('warning_msg_type_tb')

        self.error_msg_type_tb = ToggleButton(self.frame_164)
        self.horizontalLayout_128.addWidget(self.error_msg_type_tb)
        self.error_msg_type_tb.setObjectName('error_msg_type_tb')

    def set_notifications_toggle_buttons(self) -> None:
        """Sets custom widgets on settings notifications page"""
        self.image_save_notification_tb = ToggleButton(self.frame_102)
        self.horizontalLayout_85.addWidget(self.image_save_notification_tb)
        self.image_save_notification_tb.setObjectName('image_save_notification_tb')

        self.json_save_notificaion_tb = ToggleButton(self.frame_103)
        self.horizontalLayout_86.addWidget(self.json_save_notificaion_tb)
        self.json_save_notificaion_tb.setObjectName('json_save_notification_tb')

        self.secret_achievement_notification_tb = ToggleButton(self.frame_105)
        self.horizontalLayout_88.addWidget(self.secret_achievement_notification_tb)
        self.secret_achievement_notification_tb.setObjectName('secret_achievement_notification_tb')

        self.log_file_creating_notification_tb = ToggleButton(self.frame_158)
        self.horizontalLayout_129.addWidget(self.log_file_creating_notification_tb)
        self.log_file_creating_notification_tb.setObjectName('log_file_creating_notification_tb')

        self.click_link_notification_tb = ToggleButton(self.frame_106)
        self.horizontalLayout_89.addWidget(self.click_link_notification_tb)
        self.click_link_notification_tb.setObjectName('click_link_notification_tb')

        self.low_battery_notification_tb = ToggleButton(self.frame_108)
        self.horizontalLayout_90.addWidget(self.low_battery_notification_tb)
        self.low_battery_notification_tb.setObjectName('low_battery_notification_tb')

        self.high_memory_notification_tb = ToggleButton(self.frame_114)
        self.horizontalLayout_92.addWidget(self.high_memory_notification_tb)
        self.high_memory_notification_tb.setObjectName("high_memory_notification_tb")

        self.high_cpu_notification_tb = ToggleButton(self.frame_120)
        self.horizontalLayout_94.addWidget(self.high_cpu_notification_tb)
        self.high_cpu_notification_tb.setObjectName('high_cpu_notification_tb')

        self.disable_all_notification_tb = ToggleButton(self.frame_125)
        self.horizontalLayout_96.addWidget(self.disable_all_notification_tb)
        self.disable_all_notification_tb.setObjectName('disable_all_notification_tb')

    def set_appearance_toggle_buttons(self) -> None:
        """Sets toggle button on appearance settings page"""
        self.dark_left_menu_tb = ToggleButton(self.frame_27)
        self.horizontalLayout_72.addWidget(self.dark_left_menu_tb)
        self.dark_left_menu_tb.setObjectName("dark_left_menu_tb")

        self.show_address_information_tb = ToggleButton(self.frame_43)
        self.horizontalLayout_55.addWidget(self.show_address_information_tb)
        self.show_address_information_tb.setObjectName("show_address_information_tb")

        self.autoresize_map_picture_tb = ToggleButton(self.frame_55)
        self.horizontalLayout_58.addWidget(self.autoresize_map_picture_tb)
        self.autoresize_map_picture_tb.setObjectName("autoresize_map_picture_tb")

    def set_sound_toggle_buttons(self) -> None:
        """Sets toggle buttons on sounds settings page"""
        self.play_open_application_sound_tb = ToggleButton(self.frame_66)
        self.horizontalLayout_70.addWidget(self.play_open_application_sound_tb)
        self.play_open_application_sound_tb.setObjectName('play_open_application_sound_tb')

        self.play_information_dialog_sound_tb = ToggleButton(self.frame_104)
        self.horizontalLayout_165.addWidget(self.play_information_dialog_sound_tb)
        self.play_information_dialog_sound_tb.setObjectName('play_information_dialog_sound_tb')

        self.play_warning_dialog_sound_tb = ToggleButton(self.frame_62)
        self.horizontalLayout_63.addWidget(self.play_warning_dialog_sound_tb)
        self.play_warning_dialog_sound_tb.setObjectName("play_warning_dialog_sound_tb")

        self.play_error_dialog_sound_tb = ToggleButton(self.frame_159)
        self.horizontalLayout_166.addWidget(self.play_error_dialog_sound_tb)
        self.play_error_dialog_sound_tb.setObjectName("play_error_dialog_sound_tb")

        self.play_secret_achievement_sound_tb = ToggleButton(self.frame_75)
        self.horizontalLayout_73.addWidget(self.play_secret_achievement_sound_tb)
        self.play_secret_achievement_sound_tb.setObjectName('play_secret_achievement_sound_tb')

        self.disable_all_sounds_tb = ToggleButton(self.frame_77)
        self.horizontalLayout_75.addWidget(self.disable_all_sounds_tb)
        self.disable_all_sounds_tb.setObjectName("disable_all_sounds_tb")

    def set_music_toggle_buttons(self) -> None:
        """Sets toggle buttons on sounds / music settings page"""
        self.enable_music_tb = ToggleButton(self.frame_74)
        self.horizontalLayout_71.addWidget(self.enable_music_tb)
        self.enable_music_tb.setObjectName("enable_music_tb")

    def set_log_records_content_toggle_buttons(self) -> None:
        """Sets custom widgets on settings page in 'log records content'."""
        self.display_application_name_tb = ToggleButton(self.frame_170, blocked_on=True)
        self.horizontalLayout_137.addWidget(self.display_application_name_tb)
        self.display_application_name_tb.setObjectName("display_application_name_tb")

        self.display_computer_username_tb = ToggleButton(self.frame_171)
        self.horizontalLayout_144.addWidget(self.display_computer_username_tb)
        self.display_computer_username_tb.setObjectName('display_computer_username_tb')

        self.display_computer_name_tb = ToggleButton(self.frame_173)
        self.horizontalLayout_146.addWidget(self.display_computer_name_tb)
        self.display_computer_name_tb.setObjectName("display_computer_name_tb")

        self.display_recording_date_tb = ToggleButton(self.frame_174)
        self.horizontalLayout_147.addWidget(self.display_recording_date_tb)
        self.display_recording_date_tb.setObjectName("display_recording_date_tb")

        self.display_recording_time_tb = ToggleButton(self.frame_175)
        self.horizontalLayout_148.addWidget(self.display_recording_time_tb)
        self.display_recording_time_tb.setObjectName("display_recording_time_tb")

        self.display_session_id_tb = ToggleButton(self.frame_176)
        self.horizontalLayout_149.addWidget(self.display_session_id_tb)
        self.display_session_id_tb.setObjectName('display_session_id_tb')

        self.display_message_log_level_tb = ToggleButton(self.frame_177)
        self.horizontalLayout_150.addWidget(self.display_message_log_level_tb)
        self.display_message_log_level_tb.setObjectName('display_message_log_level_tb')

        self.display_message_log_name_tb = ToggleButton(self.frame_172)
        self.horizontalLayout_145.addWidget(self.display_message_log_name_tb)
        self.display_message_log_name_tb.setObjectName("display_message_log_name_tb")

        self.display_current_message_tb = ToggleButton(self.frame_178, blocked_on=True)
        self.horizontalLayout_151.addWidget(self.display_current_message_tb)
        self.display_current_message_tb.setObjectName('display_current_message_tb')

    def set_system_behaviour_toggle_buttons(self) -> None:
        """Sets toggle buttons in settings system behaviour page"""
        self.to_system_tray_tb = ToggleButton(self.frame_181)  # Todo functionality send the app to system tray when close
        self.horizontalLayout_82.addWidget(self.to_system_tray_tb)
        self.to_system_tray_tb.setObjectName("to_system_tray_tb")

    @staticmethod
    def restore_toggle_button_state(json_location: str, *toggle_buttons: tuple[ToggleButton:]) -> None:
        """Restores states of toggle buttons from .json file - json.load(APP_STATE_DATA)[json_location]"""
        for btn in toggle_buttons:
            btn.setChecked(get_json_data(APP_STATE_DATA).get(json_location, dict()).get(btn.objectName(), False))

    @property
    def notification_toggle_buttons(self) -> tuple[ToggleButton:]:
        """Returns the tuple of all toggle buttons in notification settings page"""
        return (self.image_save_notification_tb, self.json_save_notificaion_tb,
                self.secret_achievement_notification_tb, self.log_file_creating_notification_tb,
                self.click_link_notification_tb, self.low_battery_notification_tb,
                self.high_memory_notification_tb, self.high_cpu_notification_tb, self.disable_all_notification_tb)

    @property
    def log_toggle_buttons(self) -> tuple[ToggleButton:]:
        """Returns the tuple of all toggle buttons in logging settings page"""
        return (self.information_msg_type_tb, self.warning_msg_type_tb, self.error_msg_type_tb,
                self.display_computer_username_tb, self.display_application_name_tb, self.display_computer_name_tb,
                self.display_recording_time_tb, self.display_recording_date_tb, self.display_session_id_tb,
                self.display_message_log_level_tb, self.display_message_log_name_tb, self.display_current_message_tb)

    @property
    def system_behaviour_buttons(self) -> tuple[ToggleButton:]:
        """Returns the tuple of all toggle buttons in system behaviour settings page"""
        return self.to_system_tray_tb,

    @property
    def sounds_toggle_buttons(self) -> tuple[ToggleButton:]:
        return (self.play_open_application_sound_tb, self.play_information_dialog_sound_tb,
                self.play_warning_dialog_sound_tb, self.play_error_dialog_sound_tb,
                self.play_secret_achievement_sound_tb, self.disable_all_sounds_tb)

    @property
    def music_toggle_buttons(self) -> tuple[ToggleButton:]:
        return self.enable_music_tb,

    @property
    def appearance_toggle_buttons(self) -> tuple[ToggleButton:]:
        """Returns the tuple of all toggle buttons in the appearance settings page"""
        return self.dark_left_menu_tb, self.show_address_information_tb, self.autoresize_map_picture_tb

    def restore_settings_buttons_states(self) -> None:
        """Restores states of buttons from .json file"""
        data = get_json_data(APP_STATE_DATA)

        button_styles = {True: lambda btn: btn.setStyleSheet(SELECTED_CHOICE_BUTTON_STYLE),
                         False: lambda btn: btn.setStyleSheet(ORDINARY_CHOICE_BUTTON_STYLE)}
        checkmark_styles = {True: lambda check: check.setIcon(QIcon('icons/check_.png')),
                            False: lambda check: check.setIcon(QIcon(""))}

        button_styles[data.get("appearance_settings").get('dark_theme')](self.appearance_theme_dark_button)
        checkmark_styles[data.get("appearance_settings").get('dark_theme')](self.theme_dark_button_selected)

        button_styles[data.get("appearance_settings").get('light_theme')](self.appearance_theme_light_button)
        checkmark_styles[data.get("appearance_settings").get('light_theme')](self.theme_light_button_selected)

        button_styles[data.get("notification_type_settings").get("push_notification")](self.notification_push_button)
        checkmark_styles[data.get("notification_type_settings").get("push_notification")](self.notification_push_is_checked)

        button_styles[data.get("notification_type_settings").get("app_notification")](self.notification_app_button)
        checkmark_styles[data.get("notification_type_settings").get("app_notification")](self.notification_app_is_checked)


class EasterEggsFunctionality:
    """Mixin that extends the functional of a child class with EASTER EGGS"""

    def play_super_hot_scene(self) -> None:
        """Plays Easter egg SUPER HOT scene"""
        self.log_error_label.setText('')
        self.super_hot_timer.start(150)

    def write_super_hot(self) -> None:
        """Writes SUPER HOT's phrase under the lineedit"""
        phrase = "Mind Control Delete." + " " * 5  # Spaces for keeping phrase visible
        self.log_error_label.setText(phrase[0:len(self.log_error_label.text()) + 1])

        if self.log_error_label.text() == phrase or self.logFile_lineedit.text() != SUPER_HOT_EASTER_EGG:
            self.super_hot_timer.stop()
            self.log_error_label.setText("Invalid filepath")

    def android_click(self, event=None) -> None:
        """Counts the clicks on the app_version_button"""
        self.android_click_times.append(dt.now())
        if len(self.android_click_times) == 5:
            if (self.android_click_times[-1] - self.android_click_times[0]).seconds == 0:
                self.android_developer_timer.start(7)
        if len(self.android_click_times) >= 5:
            self.android_click_times.clear()

    def show_android_label(self) -> None:
        """Animates the android label appearing (vanishing)"""
        if self.android_label_alpha >= 255:
            self.android_multiplier *= -1
            self.android_reached_top = True

        if self.android_label_alpha <= 0 and self.android_reached_top:
            self.android_reached_top = False
            self.android_label_alpha = 0
            self.android_multiplier = 1
            self.android_developer_timer.stop()

        self.android_label_alpha += 3 * self.android_multiplier
        self.android_label.setStyleSheet(ANDROID_LABEL_STYLE.format(alpha=self.android_label_alpha))


class MapHelper(QMainWindow, UiFunctionality, EasterEggsFunctionality):

    morph = pymorphy2.MorphAnalyzer()
    player = QMediaPlayer()
    notificator = ToastNotifier()

    def __init__(self):
        super().__init__()
        uic.loadUi("main_interface.ui", self)

        # Main data
        self.request_get = connecting_get(self.connect_warn)(get)
        self.image_types = {"Standard map": 'map', "Hybrid": "sat,skl", "Satellite": "sat"}
        self.system_languages = {"Russian": "ru_RU", "English": "en_US"}
        self.system_functions = self.showMaximized, self.showNormal
        self.resize_buttons = ('icons/maximize.png', 'icons/resize_1.png')
        self.current_system_function, self.current_resize_button_icon = 0, 1
        self.longitude, self.latitude, self.scale = None, None, None
        self.user_json_file, self.user_image_file, self.current_bytes_image, self.json_data = None, None, None, None
        self.image_url_pattern = re.compile(r"background-image:\s?(url\(.+\))")
        self.session_id = f"{dt.now().strftime('%f%S%M%H%d%m%Y')}"
        self.pressed_keys = list()

        # Groups of buttons (to make an effect of multiple choice of many buttons)
        self.settings_appearance_theme_buttons = {self.appearance_theme_light_button: self.theme_light_button_selected,
                                                  self.appearance_theme_dark_button: self.theme_dark_button_selected}

        self.settings_type_notification_buttons = {self.notification_push_button: self.notification_push_is_checked,
                                                   self.notification_app_button: self.notification_app_is_checked}

        for button in self.settings_appearance_theme_buttons:
            button.clicked.connect(lambda: self.change_styles(self.settings_appearance_theme_buttons))

        for button in self.settings_type_notification_buttons:
            button.clicked.connect(lambda: self.change_styles(self.settings_type_notification_buttons))

        # CPU, RAM states
        self.latest_cpu_values, self.latest_ram_values = [], []

        # Delta-timers
        self.delta_timer_cpu = self.delta_timer_ram = self.delta_timer_battery = dt.now()

        # Timers
        self.cpu_timer = QTimer()
        self.cpu_timer.timeout.connect(self.pc_state_update)
        self.cpu_timer.start(750)

        self.super_hot_timer = QTimer()
        self.super_hot_timer.timeout.connect(self.write_super_hot)

        self.android_developer_timer = QTimer()
        self.android_developer_timer.timeout.connect(self.show_android_label)

        self.state_timer = QTimer()
        self.state_timer.timeout.connect(self.check_pc_state)
        self.state_timer.start(1000)

        self.block_label_timer = QTimer()
        self.block_label_timer.timeout.connect(lambda: self.change_blocking_label_transparency())
        self.block_label_alpha = 0

        # Easter egg data
        self.android_click_times = []
        self.android_label_alpha = 0
        self.android_multiplier = 1
        self.android_reached_top = False

        self.track_buttons_to_stop_onestop = False

        # Computer state
        self.current_cpu_usage = 0
        self.current_ram_usage = 0
        self.current_battery_charge = 100

        # Variables to control animations
        self.is_on_settings_frame = False

        # Centering the window
        frame = self.frameGeometry()
        frame.moveCenter(QDesktopWidget().availableGeometry().center())
        self.move(frame.topLeft())

        # Setting up the background properties
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # System button
        self.resize_window_system_button.clicked.connect(self.resize_window)
        self.minimize_window_system.clicked.connect(lambda: self.showMinimized())
        self.close_window_system.clicked.connect(lambda: self.close())

        # Make line_edits empty
        self.empty_longitude_button.clicked.connect(lambda: self.longitude_lineedit.setText(''))
        self.empty_lattitude_button.clicked.connect(lambda: self.lattitude_lineedit.setText(''))
        self.empty_address_butt.clicked.connect(lambda: self.address_lineedit.setText(''))
        self.clear_scale_btn.clicked.connect(lambda: self.scale_lineedit.setText(''))
        self.empty_logfile_button.clicked.connect(lambda: self.logFile_lineedit.setText(''))
        self.empty_records_number.clicked.connect(lambda: self.rows_num_lineedit.setText(''))

        # Check correct input
        self.lattitude_lineedit.textChanged.connect(self.check_correct_input_lattitude)
        self.image_combobox.currentTextChanged.connect(self.change_image_property)
        self.lang_combobox.currentTextChanged.connect(self.change_image_property)
        self.longitude_lineedit.textChanged.connect(self.check_correct_input_longitude)
        self.address_lineedit.textChanged.connect(self.check_correct_input_address)
        self.scale_lineedit.textChanged.connect(self.check_correct_input_scale)

        # Random values
        self.random_lattitude_button.clicked.connect(lambda: self.lattitude_lineedit.setText(f"{round(random.uniform(-89.999, 89.999), 6)}"))
        self.random_longitude_button.clicked.connect(lambda: self.longitude_lineedit.setText(f"{round(random.uniform(-179.99, 179.99), 6)}"))
        self.random_address_button.clicked.connect(lambda: self.address_lineedit.setText(self.random_address))

        # Search button
        self.search_longitude_button.clicked.connect(self.search_coords)
        self.search_lattitude_button.clicked.connect(self.search_coords)
        self.search_address_button.clicked.connect(self.search_address)

        # Left-menu buttons
        self.menu_button.clicked.connect(self.toggle_left_menu)
        self.home_button.clicked.connect(lambda: self.stacked.setCurrentIndex(0))
        self.point_button.clicked.connect(lambda: self.stacked.setCurrentIndex(3))
        self.line_button.clicked.connect(lambda: self.stacked.setCurrentIndex(2))
        self.gear_button.clicked.connect(lambda: self.stacked.setCurrentIndex(4))
        self.info_button.clicked.connect(lambda: self.stacked.setCurrentIndex(1))

        # Left-menu settings buttons
        self.settings_appearance_btn.clicked.connect(lambda: self.settings_stacked_widget.setCurrentIndex(0))
        self.settings_notifications_btn.clicked.connect(lambda: self.settings_stacked_widget.setCurrentIndex(2))
        self.settings_sounds_btn.clicked.connect(lambda: self.settings_stacked_widget.setCurrentIndex(1))
        self.settigns_windows_btn.clicked.connect(lambda: self.settings_stacked_widget.setCurrentIndex(3))

        # Event log settings
        self.logFile_lineedit.textChanged.connect(self.check_correct_input_logfile)
        self.rows_num_lineedit.textChanged.connect(self.check_correct_input_records_number)

        # Changing text of widgets
        self.python_btn.setText(PYTHON_LINK)
        self.sql_btn.setText(SQL_LINK)
        self.qtDesigner_btn.setText(QT_LINK)
        self.logFile_lineedit.setPlaceholderText(os.environ["USERPROFILE"])
        self.current_user_button.setText(F"Current user: {os.environ['USERNAME']}")
        self.current_system_version.setText(f"{platform.system()} {platform.release()} {os.environ['PROCESSOR_ARCHITECTURE'][-2:]}-bit ({platform.win32_ver()[1]})")
        file = get_json_data(USER_JSON_DATA).get("log_file", "")
        self.logFile_lineedit.setText(file if os.path.exists(file) else '')

        max_records_number = get_json_data(USER_JSON_DATA).get('records_number', None)
        self.rows_num_lineedit.setText(str(max_records_number) if isinstance(max_records_number, int) else "")

        # Other buttons
        self.python_btn.clicked.connect(lambda: self.follow_link(self.sender().text()))
        self.qtDesigner_btn.clicked.connect(lambda: self.follow_link(self.sender().text()))
        self.sql_btn.clicked.connect(lambda: self.follow_link(self.sender().text()))
        self.save_image_button.clicked.connect(self.save_map_image)
        self.save_json_file_button.clicked.connect(self.save_json_file)
        self.web_search_button.clicked.connect(self.web_search)
        self.address_button.clicked.connect(self.copy_address)
        self.coordinates_button.clicked.connect(self.copy_coordinates)
        self.postal_code_btn.clicked.connect(self.copy_post_code)
        self.btn_vk.clicked.connect(lambda: wb.open(f"https://vk.com/liminnium"))  # todo other social media
        self.open_logfile_button.clicked.connect(self.open_logfile)
        self.apply_log_settings_button.clicked.connect(self.apply_log_settings)
        self.reset_log_settings_button.clicked.connect(self.reset_log_settings)

        # Setting and customizing custom widgets
        self.cpu_bar = CircularProgress(0, width=150, height=150, progress_width=7, font_size=18, enable_shadow=False,
                                        color_of_progress=(189, 147, 249), bg_color=(65, 65, 85))
        self.cpu_bar.move(24, 18)
        self.cpu_bar.setParent(self.cpu_progressbar_frame)

        self.ram_bar = CircularProgress(0, width=150, height=150, progress_width=7, font_size=18, enable_shadow=False,
                                        color_of_progress=(189, 147, 249), bg_color=(65, 65, 85))
        self.ram_bar.move(24, 18)
        self.ram_bar.setParent(self.ram_progressbar_frame)

        self.add_shadows(self.address_field_frame, self.lattitude_field_frame, self.longitude_field_frame,
                         self.image_field_frame, self.language_field_frame, self.scale_coefficient_frame,
                         shadow_color=(0, 0, 0, 70), blurring=20, x_offset=0, y_offset=0)

        self.app_version_button.mousePressEvent = self.android_click

        self.id_button.setText(self.session_id)
        self.id_button.clicked.connect(self.copy_session_id)

        # Setting properties of some widgets
        for child in self.leftmenu_frame.children():
            if isinstance(child, QPushButton) and child.objectName() != "menu_button":
                child.clicked.connect(self.set_selected_style)
                child.clicked.connect(self.toggle_left_menu)

        self.restore_settings_buttons_states()

        self.set_display_msg_types_toggle_buttons()
        self.set_notifications_toggle_buttons()
        self.set_system_behaviour_toggle_buttons()
        self.set_log_records_content_toggle_buttons()
        self.set_appearance_toggle_buttons()
        self.set_sound_toggle_buttons()
        self.set_music_toggle_buttons()

        self.restore_toggle_button_state('log_settings', *self.log_toggle_buttons)
        self.restore_toggle_button_state('notification_messages_settings', *self.notification_toggle_buttons)
        self.restore_toggle_button_state("system_behaviour_settings", *self.system_behaviour_buttons)
        self.restore_toggle_button_state("sound_settings", *self.sounds_toggle_buttons)
        self.restore_toggle_button_state('music_settings', *self.music_toggle_buttons)
        self.restore_toggle_button_state("appearance_settings", *self.appearance_toggle_buttons)

        for slider in (self.cpu_slider, self.ram_slider):
            slider.setMinimum(50)
            slider.setMaximum(100)
        self.battery_slider.setMinimum(0)
        self.battery_slider.setMaximum(50)
        self.music_slider.setMinimum(0)
        self.music_slider.setMaximum(100)

        self.ram_slider.setValue(get_json_data(APP_STATE_DATA).get("notification_messages_settings", {}).get(self.ram_slider.objectName(), 50))
        self.cpu_slider.setValue(get_json_data(APP_STATE_DATA).get("notification_messages_settings", {}).get(self.cpu_slider.objectName(), 50))
        self.battery_slider.setValue(get_json_data(APP_STATE_DATA).get("notification_messages_settings", {}).get(self.battery_slider.objectName(), 0))
        self.music_slider.setValue(get_json_data(APP_STATE_DATA).get('music_settings', {}).get(self.music_slider.objectName(), 0))

        for slider in (self.cpu_slider, self.battery_slider, self.ram_slider, self.music_slider):
            slider.setToolTip(f"Current percent: {slider.value()}%")
            slider.valueChanged.connect(lambda: self.sender().setToolTip(f'Current percent: {self.sender().value()}%'))

        self.disable_all_notification_tb.stateChanged.connect(lambda: self.disable_toggle_buttons(self.notification_toggle_buttons))
        self.disable_all_sounds_tb.stateChanged.connect(lambda: self.disable_toggle_buttons(self.sounds_toggle_buttons))

        # Instances
        self.logger = Logger(get_json_data(USER_JSON_DATA).get('log_file'),
                             get_json_data(USER_JSON_DATA).get("records_number"), CODING,
                             self.information_msg_type_tb.isChecked(),
                             self.warning_msg_type_tb.isChecked(),
                             self.error_msg_type_tb.isChecked(),
                             app_name=getattr(type(self), "__name__"),
                             computer_user=os.environ["USERNAME"],
                             computer_name=os.environ["COMPUTERNAME"],
                             session_id=self.session_id)

        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon(APP_ICON))
        self.tray_icon.setToolTip(f"MapHelper — your wise geo-advice")

        show_action = QAction("Show", self)
        show_action.setIcon(QIcon(SHOW_APP_ICON))
        show_action.triggered.connect(self.show)

        hide_action = QAction("Hide", self)
        hide_action.setIcon(QIcon(HIDE_APP_ICON))
        hide_action.triggered.connect(self.hide)

        quit_action = QAction("Exit", self)
        quit_action.setIcon(QIcon(EXIT_APP_ICON))
        quit_action.triggered.connect(qApp.quit)

        tray_menu = QMenu()
        tray_menu.setStyleSheet(TRAY_MENU_STYLE)
        tray_menu.addActions((show_action, hide_action, quit_action))
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(lambda event: self.show() if event == 3 else None)
        self.tray_icon.show()

        self.block_label = QLabel(self)  # Label that appears when time_here_dialog appears
        self.block_label.resize(self.size())  # Makes the screen blurred
        self.block_label.move(0, 0)
        self.block_label.hide()

        # Toggle buttons
        self.information_msg_type_tb.stateChanged.connect(lambda: self.logger.change_properties(info_on=self.information_msg_type_tb.isChecked()))
        self.warning_msg_type_tb.stateChanged.connect(lambda: self.logger.change_properties(warning_on=self.warning_msg_type_tb.isChecked()))
        self.error_msg_type_tb.stateChanged.connect(lambda: self.logger.change_properties(error_on=self.error_msg_type_tb.isChecked()))

        # Resize window by double click
        self.title_name.mouseDoubleClickEvent = self.resize_window
        # Make windows draggable with title bar
        self.title_name.mouseMoveEvent = self.move_window

        # Make settings left menu shrinkable
        self.settings_left_manu_frame.leaveEvent = self.shrink_setting_leftmenu
        self.extend_menu.clicked.connect(self.extend_setting_leftmenu)

        # Logging and playing sound
        self.log_record("MapHelper is opened.", "info")  # Logging
        self.play_audio(OPEN_SOUND)

        # Increasing number of opens
        self.current_times_here = get_json_data(USER_JSON_DATA).get('time_heres', 0) + 1
        write_json_data(filename=USER_JSON_DATA, **{"time_heres": self.current_times_here})

    def get_image(self, longitude: float, latitude: float, spn: float) -> bytes:
        """Gets bytes array of the image from Yandex.Maps API"""
        response = self.request_get("http://static-maps.yandex.ru/1.x",
                                    params={'ll': ','.join(map(str, (longitude, latitude))),
                                            'spn': ','.join(map(str, (spn, spn))),
                                            'l': self.image_types[self.image_combobox.currentText()],
                                            "size": f'{self.image.width()},{self.image.height()}',
                                            "lang": self.system_languages[self.lang_combobox.currentText()]},
                                    timeout=0.5)

        if not response:
            self.log_record(f"Image was not displayed. Status: {response.status_code}. Reason: {response.reason}.",
                            "error")  # Logging
            return bytes()

        self.current_bytes_image = response.content
        return response.content

    @staticmethod
    def make_image(data: bytes) -> None:
        """Запись в файл потока байтов"""
        with open(FILE_IMAGE_NAME, mode="wb") as file:
            file.write(data)

    @property
    def toponym_coords(self) -> str:
        """Get coordinates of the current toponym"""
        toponym = self.json_data["response"]["GeoObjectCollection"]["featureMember"][0]
        return re.sub(r"\s", ', ', toponym["GeoObject"]["Point"]["pos"]).__str__()

    @property
    def toponym_postal_code(self) -> str:
        """Get postal code of the current toponym"""
        toponym = self.json_data["response"]["GeoObjectCollection"]["featureMember"][0]
        return toponym["GeoObject"]["metaDataProperty"]["GeocoderMetaData"]["Address"].get("postal_code", None)

    @property
    def toponym_address(self) -> str:
        """Get address of the current toponym"""
        toponym = self.json_data["response"]["GeoObjectCollection"]["featureMember"][0]
        return toponym["GeoObject"]["metaDataProperty"]["GeocoderMetaData"]["text"]

    def change_image_property(self) -> None:
        """Changing image properties"""
        if self.latitude is not None:
            self.make_image(self.get_image(self.longitude, self.latitude, self.scale))
            self.image.setPixmap(QPixmap(FILE_IMAGE_NAME))

    def check_correct_input_longitude(self) -> bool:
        """Checks the validness of the specified longitude"""
        valid_types = (r"\d|-", r"\d|[.,;:]", r"\d|[.,;:]", r"\d|[.,;:]", r"\d|[,.;:]", r"\d")

        long_text = self.longitude_lineedit.text().strip()
        if long_text and not (
                all((re.fullmatch(valid_types[min(5, i)], long_text[i]) for i in range(len(long_text))))
                and len(re.findall(r"[.,;:]", long_text)) <= 1 and long_text.count('-') <= 1):
            self.longitude_icon_error.setStyleSheet(WARNING_ICON)
            self.longitude_error_label.setText(f"Invalid format")
            self.longitude_lineedit.setStyleSheet(ERROR_LINEEDIT_STYLE)
            return False

        if (len(long_text) > 10 and not long_text.startswith('-')) or (len(long_text) > 11 and long_text.startswith('-')):
            self.longitude_icon_error.setStyleSheet(WARNING_ICON)
            self.longitude_error_label.setText(f"Value is too long")
            self.longitude_lineedit.setStyleSheet(ERROR_LINEEDIT_STYLE)
            return False

        if len(long_text) > 1:
            if abs(float(re.sub(r"[,;:]", ".", long_text))) > 179.999:
                if long_text[0] == '-':
                    self.longitude_icon_error.setStyleSheet(WARNING_ICON)
                    self.longitude_error_label.setText(f"Value is too small")
                    self.longitude_lineedit.setStyleSheet(ERROR_LINEEDIT_STYLE)
                    return False
                self.longitude_icon_error.setStyleSheet(WARNING_ICON)
                self.longitude_error_label.setText(f"Value is too large")
                self.longitude_lineedit.setStyleSheet(ERROR_LINEEDIT_STYLE)
                return False

        self.longitude_icon_error.setStyleSheet("image: none")
        self.longitude_error_label.setText("")
        self.longitude_lineedit.setStyleSheet(ORDINARY_LINEEDIT_STYLE)

        return True

    def check_correct_input_lattitude(self) -> bool:
        """Checks the validness of the specified latitude"""
        valid_types = (r"\d|-", r"\d|[.,;:]", r"\d|[.,;:]", r"\d|[.,;:]", r"\d|[,.;:]", r"\d")

        lat_text = self.lattitude_lineedit.text().strip()

        # Reset address input field error/warning style
        ...  # ToDo

        if lat_text and not (
                all((re.fullmatch(valid_types[min(5, i)], lat_text[i]) for i in range(len(lat_text))))
                and len(re.findall(r"[.,;:]", lat_text)) <= 1 and lat_text.count('-') <= 1):
            self.lattitude_lineedit.setStyleSheet(ERROR_LINEEDIT_STYLE)
            self.lattitude_icon_error.setStyleSheet(WARNING_ICON)
            self.lattitude_error_label.setText(f"Invalid format")
            return False

        if len(lat_text) > 10:
            self.lattitude_lineedit.setStyleSheet(ERROR_LINEEDIT_STYLE)
            self.lattitude_icon_error.setStyleSheet(WARNING_ICON)
            self.lattitude_error_label.setText(f"Value is too long")
            return False

        if len(lat_text) > 1:
            if abs(float(re.sub(r"[,;:]", ".", lat_text))) > 89.999:
                if lat_text[0] == '-':
                    self.lattitude_lineedit.setStyleSheet(ERROR_LINEEDIT_STYLE)
                    self.lattitude_icon_error.setStyleSheet(WARNING_ICON)
                    self.lattitude_error_label.setText(f"Value is too small")
                    return False
                self.lattitude_lineedit.setStyleSheet(ERROR_LINEEDIT_STYLE)
                self.lattitude_icon_error.setStyleSheet(WARNING_ICON)
                self.lattitude_error_label.setText(f"Value is too large")
                return False

        self.lattitude_lineedit.setStyleSheet(ORDINARY_LINEEDIT_STYLE)
        self.lattitude_icon_error.setStyleSheet('image: none')
        self.lattitude_error_label.setText("")

        return True

    def check_correct_input_address(self) -> bool:
        """Checks the validness of the specified address"""
        address_text = self.address_lineedit.text().strip()

        if any(ec in string.ascii_letters for ec in address_text) and any(rc in RUSSIAN_LETTERS for rc in address_text):
            self.address_error_label.setText("Address contains letters of different languages")
            return False

        if address_text:
            if not re.fullmatch(r"[0-9А-Я-A-ZЁ/№# .,;_-]+", address_text, flags=re.I):
                self.address_error_label.setText("Address may contain incorrect symbols")
                return False

        if len(address_text) > 3:
            if re.fullmatch(r"[^A-ZА-Я]+", address_text, flags=re.IGNORECASE):
                self.address_error_label.setText("Address may be incorrect")
                return False

        self.address_error_label.setStyleSheet(WARNING_TITLE_STYLE)
        self.address_error_label.setText('')
        self.address_icon_error.setStyleSheet("image: none")
        self.address_lineedit.setStyleSheet(ORDINARY_LINEEDIT_STYLE)
        return True

    def check_correct_input_scale(self) -> bool:
        """Checks validness of the specified scale coefficient"""
        valid_types = (r'\d', r'\d|[,.;:]', r'\d|[,.:;]', r'\d')

        scale = self.scale_lineedit.text().strip()

        if scale and not (all((re.fullmatch(valid_types[min(3, i)], scale[i]) for i in range(len(scale)))) and
                          len(re.findall(r"\d", scale)) >= len(scale) - 1):
            self.scale_icon_error.setStyleSheet(WARNING_ICON)
            self.scale_lineedit.setStyleSheet(ERROR_LINEEDIT_STYLE)
            self.scale_error_label.setText("Invalid format")
            return False

        if len(re.findall(r'\d', scale)) > 7:
            self.scale_icon_error.setStyleSheet(WARNING_ICON)
            self.scale_lineedit.setStyleSheet(ERROR_LINEEDIT_STYLE)
            self.scale_error_label.setText("Too long value")
            return False

        if scale:
            if float(re.sub(r"[,.;:]", ".", scale)) > 99:
                self.scale_icon_error.setStyleSheet(WARNING_ICON)
                self.scale_lineedit.setStyleSheet(ERROR_LINEEDIT_STYLE)
                self.scale_error_label.setText("Too large number")
                return False

        self.scale_error_label.setText('')
        self.scale_lineedit.setStyleSheet(ORDINARY_LINEEDIT_STYLE)
        self.scale_icon_error.setStyleSheet("image: none")

        return True

    def check_correct_input_logfile(self) -> bool:
        """Checks validness of the specified name of log file"""
        log_file = self.logFile_lineedit.text()

        if log_file == SUPER_HOT_EASTER_EGG:  # EASTER EGG
            self.play_super_hot_scene()
            return False

        if log_file:
            if not re.match(r"^[a-z]:(\\|/)", log_file, flags=re.IGNORECASE) or re.search(r'(\\|/){2,}', log_file) \
                    or any(c in WINDOWS_FORBIDDEN_SYMBOLS for c in log_file):
                self.logfile_icon_error.setStyleSheet(WARNING_ICON)
                self.logFile_lineedit.setStyleSheet(ERROR_LINEEDIT_STYLE)
                self.log_error_label.setText("Invalid filepath")
                return False

            if not re.search(r'((\\|/)[^\n]+\.[a-z0-9]{2,})$', log_file, flags=re.IGNORECASE):
                self.logfile_icon_error.setStyleSheet(WARNING_ICON)
                self.logFile_lineedit.setStyleSheet(ERROR_LINEEDIT_STYLE)
                self.log_error_label.setText("Log-file is not specified")
                return False

            if not pathlib.Path(pathlib.Path(log_file).parent).exists():
                self.logfile_icon_error.setStyleSheet(WARNING_ICON)
                self.logFile_lineedit.setStyleSheet(ERROR_LINEEDIT_STYLE)
                self.log_error_label.setText("Log-file folder does not exist")
                return False

            if not log_file[log_file.rfind('.'):] in LOG_FILE_EXTENSIONS:
                self.logfile_icon_error.setStyleSheet(WARNING_ICON)
                self.logFile_lineedit.setStyleSheet(ERROR_LINEEDIT_STYLE)
                self.log_error_label.setText(f"Log-file must be "
                                             f"{', '.join(LOG_FILE_EXTENSIONS[:-1])} or {LOG_FILE_EXTENSIONS[-1]}")
                return False

        self.logfile_icon_error.setStyleSheet("image: none")
        self.logFile_lineedit.setStyleSheet(ORDINARY_LINEEDIT_STYLE)
        self.log_error_label.setText("")

        return True

    def check_correct_input_records_number(self) -> bool:
        """Checks validness of specified number of records"""
        records_number = self.rows_num_lineedit.text()

        if records_number:
            if records_number.startswith('0') or re.search(r'\D', records_number):
                self.rows_num_lineedit.setStyleSheet(ERROR_LINEEDIT_STYLE)
                self.records_number_error_icon.setStyleSheet(WARNING_ICON)
                self.records_number_error.setText("Invalid value")
                return False

            if int(records_number) > pow(2, 14):
                self.rows_num_lineedit.setStyleSheet(ERROR_LINEEDIT_STYLE)
                self.records_number_error_icon.setStyleSheet(WARNING_ICON)
                self.records_number_error.setText("Too large value")
                return False

        self.rows_num_lineedit.setStyleSheet(ORDINARY_LINEEDIT_STYLE)
        self.records_number_error_icon.setStyleSheet("image: none")
        self.records_number_error.setText("")
        return True

    def open_logfile(self) -> None:
        """Opens the log-file and writes the absolute path in the corresponding lineedit"""

        extensions = ";;".join(map(lambda i: f"Log-file (*{i})", LOG_FILE_EXTENSIONS))
        log_file_location = QFileDialog.getOpenFileName(self, "Select log-file...", "", extensions)[0]

        if log_file_location:
            self.logFile_lineedit.setText(log_file_location)

    def search_coords(self) -> None:
        """Searches the toponym (with coordinates)"""
        validness_is_not_ok = False

        if not self.longitude_lineedit.text().split() or not self.check_correct_input_longitude():
            if self.check_correct_input_longitude():
                self.longitude_icon_error.setStyleSheet(WARNING_ICON)
                self.longitude_error_label.setText(f"Longitude is required")
                self.longitude_lineedit.setStyleSheet(ERROR_LINEEDIT_STYLE)
            validness_is_not_ok = True

        if not self.lattitude_lineedit.text().split() or not self.check_correct_input_lattitude():
            if self.check_correct_input_lattitude():
                self.lattitude_icon_error.setStyleSheet(WARNING_ICON)
                self.lattitude_error_label.setText(f"Latitude is required")
                self.lattitude_lineedit.setStyleSheet(ERROR_LINEEDIT_STYLE)
            validness_is_not_ok = True

        if not self.scale_lineedit.text() or not self.check_correct_input_scale():
            if self.check_correct_input_scale():
                self.scale_error_label.setText(f"Scale coefficient is required")
                self.scale_lineedit.setStyleSheet(ERROR_LINEEDIT_STYLE)
                self.scale_icon_error.setStyleSheet(WARNING_ICON)
            validness_is_not_ok = True

        # If something is wrong, return out
        if validness_is_not_ok:
            return

        self.longitude = float(re.sub(r'[,;:]', r".", self.longitude_lineedit.text()))
        self.latitude = float(re.sub(r'[,;:]', r".", self.lattitude_lineedit.text()))
        self.scale = float(re.sub(r'[,;:]', r".", self.scale_lineedit.text()))

        temp_data = self.request_get('http://geocode-maps.yandex.ru/1.x',
                                     params={'apikey': GEOCODE_APIKEY,
                                             'format': 'json',
                                             'geocode': f"{self.longitude},{self.latitude}"})
        if temp_data is None:
            return

        self.json_data = temp_data.json()

        self.address_button.setText(f"Current address: {self.toponym_address if len(self.toponym_address) < 25 else self.toponym_address[:22] + '...'}")
        self.coordinates_button.setText(f"Current coordinates: {self.toponym_coords}")
        self.postal_code_btn.setText(f"Postal code: {self.toponym_postal_code if self.toponym_postal_code is not None else 'No postal code'}")

        self.make_image(self.get_image(self.longitude, self.latitude, self.scale))
        self.image.setPixmap(QPixmap(FILE_IMAGE_NAME))

        self.log_record("Image ({0}) displayed correctly.".format(self.toponym_coords), "info")  # Logging

    def notify(self, title, msg, show, *, icon_path: str = f"{os.getcwd()}/images/image.ico", duration: int = 7,
               threaded: bool = True, callback_on_click: (FunctionType, MethodType) = None) -> None:
        """Sends the notification of an action depends on specified type of notifications"""

        if not show:  # show parameter is a parameter that takes the value of state of current toggle button
            return

        # Different notifications depends on specified notification type
        if get_json_data(APP_STATE_DATA).get('notification_type_settings', dict()).get("push_notification", False):  # Push
            self.notificator.show_toast(title, msg, icon_path, duration, threaded, callback_on_click)
        else:  # Todo app-not.
            pass

    def search_address(self) -> None:
        """Searches the toponym (with address)"""
        _return = False

        if not self.address_lineedit.text().split():
            self.address_lineedit.setStyleSheet(ERROR_LINEEDIT_STYLE)
            self.address_error_label.setStyleSheet(ERROR_TITLE_STYLE)
            self.address_error_label.setText("Address is required")
            self.address_icon_error.setStyleSheet(WARNING_ICON)
            _return = True

        if self.address_lineedit.text() == ONESTOPMID:  # EASTER EGG!!!
            self.play_audio(ONESTOP_SOUND)
            self.address_lineedit.setText("")
            self.track_buttons_to_stop_onestop = True
            return

        if not self.scale_lineedit.text() or not self.check_correct_input_scale():
            if self.check_correct_input_scale():
                self.scale_error_label.setText(f"Scale coefficient is required")
                self.scale_lineedit.setStyleSheet(ERROR_LINEEDIT_STYLE)
                self.scale_icon_error.setStyleSheet(WARNING_ICON)
            _return = True

        # Если проверка на корректность не прошла, выбрасывать прочь из функции
        if _return:
            return

        self.address_error_label.setStyleSheet(WARNING_TITLE_STYLE)

        temp_data = self.request_get('http://geocode-maps.yandex.ru/1.x',
                                     params={'format': 'json',
                                             'apikey': GEOCODE_APIKEY,
                                             'geocode': self.address_lineedit.text()},
                                     timeout=.5)
        if temp_data is None:
            return

        self.json_data = temp_data.json()

        # Если изображение не нашлось
        if self.json_data["response"]["GeoObjectCollection"]["metaDataProperty"]["GeocoderResponseMetaData"]["found"] == '0':
            self.address_icon_error.setStyleSheet(WARNING_ICON)
            self.address_error_label.setStyleSheet(ERROR_TITLE_STYLE)
            self.address_error_label.setText("No results for current address")
            self.log_record("No results for current address.", "warning")  # Logging
            return

        toponym = self.json_data["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        self.longitude, self.latitude = map(float, toponym['Point']["pos"].split())
        self.scale = float(re.sub(r'[,;:]', r".", self.scale_lineedit.text()))

        self.address_button.setText(f"Current address: {self.toponym_address if len(self.toponym_address) < 25 else self.toponym_address[:22] + '...'}")
        self.coordinates_button.setText(f"Current coordinates: {self.toponym_coords}")
        self.postal_code_btn.setText(f"Postal code: {self.toponym_postal_code if self.toponym_postal_code is not None else 'No postal code'}")

        self.make_image(self.get_image(self.longitude, self.latitude, self.scale))
        self.image.setPixmap(QPixmap(FILE_IMAGE_NAME))

        self.log_record("Image ({0}) displayed correctly.".format(self.toponym_coords), "info")  # Logging

    def web_search(self) -> None:
        """Web-searches the toponym"""
        if self.json_data is None:
            self.play_audio(WARNING_SOUND)
            pop_up = WarningDialog("Web-search", "Search for a toponym before.", "icons/warning_icon_dialog.png")
            pop_up.exec()
            return

        curtoponym = self.json_data["response"]["GeoObjectCollection"]["featureMember"][0]
        address_component = {my_dict["kind"]: my_dict["name"] for my_dict in
                             curtoponym["GeoObject"]["metaDataProperty"]["GeocoderMetaData"]["Address"]["Components"]}

        if 'hydro' in address_component:
            toponym_name = address_component['hydro']

        if 'country' in address_component:
            toponym_name = address_component["country"]

        if 'province' in address_component:
            toponym_name = address_component["province"]

        if "locality" in address_component:
            toponym_name = address_component["locality"]

        toponym_name = re.sub(r'(?:город|провинция|село)', "", toponym_name, flags=re.IGNORECASE)

        if self.webbrowser_search_combobox.currentText() == 'Historical information':
            link = f"https://ru.wikipedia.org/wiki/{toponym_name}#История"
        elif self.webbrowser_search_combobox.currentText() == "Main information":
            link = f"https://ru.wikipedia.org/wiki/{toponym_name}"
        elif self.webbrowser_search_combobox.currentText() == "Attraction":
            object_name = list(self.morph.parse(toponym_name)[0].inflect({'gent'})[0])

            # Changing case of letters in the changed form of the name of the toponym
            for index, char in enumerate(toponym_name):
                if object_name[index].lower() == char.lower():
                    if char.isupper():
                        object_name[index] = char.upper()

            # Changing case of letters in changed form of the name of the toponym
            # in different order (from -1 index to -len)
            for index in range(-1, len(toponym_name) * -1, -1):
                if object_name[index].lower() == toponym_name[index].lower():
                    if toponym_name[index].isupper():
                        object_name[index] = toponym_name[index].upper()

            link = f"https://ru.wikipedia.org/wiki/Категория:Достопримечательности_{''.join(object_name).strip()}"

        self.follow_link(link)
        self.log_record(f'Followed ({link}) link.', "info")  # Logging

    def save_map_image(self) -> None:
        """Saves current image as a file"""
        if self.current_bytes_image is None:
            self.play_audio(WARNING_SOUND)
            pop_up = WarningDialog("Saving image", "No image to save.", "icons/warning_icon_dialog.png")
            pop_up.exec()
            return

        self.user_image_file = QFileDialog.getSaveFileName(self, "Save image as...", self.toponym_address[:50],
                                                           'Image (*.png);;Image (*.jpg);;'
                                                           'Image (*.jpeg);;Image (*.bmp);;'
                                                           'Image (*.svg);;Image (*.webp)')[0]

        # If saving was cancelled
        if not self.user_image_file:
            return

        with open(self.user_image_file, mode='wb') as fp:
            fp.write(self.current_bytes_image)

        # Check if the file was actually created
        if os.path.getsize(self.user_image_file):
            file_name = pathlib.Path(self.user_image_file).name
            self.log_record(f"Image file ({file_name}) was saved.", "info")  # Logging
            self.notify(f'Image file "{file_name[:9] + "..." + file_name[-9:] if len(file_name) > 21 else file_name}" was saved.',
                        "Click to remove...",
                        (self.image_save_notification_tb.isChecked() and not self.disable_all_notification_tb.isChecked()),
                        callback_on_click=lambda: self.remove_created_file(self.user_image_file, "Image"))

    def save_json_file(self) -> None:
        """Saves the json file of got image"""
        if self.json_data is None:
            self.play_audio(WARNING_SOUND)
            WarningDialog("Saving JSON file", "No JSON data to save.", "icons/warning_icon_dialog.png").exec()
            return

        self.user_json_file = QFileDialog.getSaveFileName(self, "Save JSON as...",
                                                          self.toponym_address[:50], "File (*.json)")[0]

        if not self.user_json_file:
            return

        with open(self.user_json_file, mode='w', encoding=CODING) as fp:
            json.dump(self.json_data, fp, indent=4, ensure_ascii=False)

        if os.path.getsize(self.user_json_file):
            file_name = pathlib.Path(self.user_json_file).name
            self.log_record(f"JSON file ({file_name}) was saved.", "info")  # Logging
            self.notify(f'JSON file "{file_name[:9] + "..." + file_name[-9:] if len(file_name) > 21 else file_name}" was saved.',
                        "Click to remove...",
                        (self.json_save_notificaion_tb.isChecked() and not self.disable_all_notification_tb.isChecked())
                        , callback_on_click=lambda: self.remove_created_file(self.user_json_file, "JSON"))

    def show_easter_egg(self):
        self.block_label_alpha = 0

        self.block_label.show()

        self.block_label_timer.disconnect()
        self.block_label_timer.timeout.connect(lambda: self.change_blocking_label_transparency())

        self.block_label_timer.start(7)

        EasterEggDialog().exec()

        self.block_label_timer.timeout.disconnect()
        self.block_label_timer.timeout.connect(lambda: self.change_blocking_label_transparency(reverse=True))
        self.block_label_timer.start(7)

    def resize_window(self, event=None) -> None:
        """Changing the size of the window"""
        self.resize_window_system_button.setIcon(QIcon(self.resize_buttons[self.current_resize_button_icon % 2]))
        self.system_functions[self.current_system_function % 2]()

        if self.current_resize_button_icon % 2:
            self.resize_window_system_button.setIconSize(QSize(32, 32))
        else:
            self.resize_window_system_button.setIconSize(QSize(21, 21))

        self.current_resize_button_icon += 1
        self.current_system_function += 1

    def change_blocking_label_transparency(self, reverse: bool = False):
        """Changes the transparency of the blocking label"""
        self.block_label_alpha += 1 if not reverse else -1
        self.block_label.setStyleSheet(BLOCKING_LABEL_STYLE.format(alpha=self.block_label_alpha))

        if not reverse and self.block_label_alpha == 50:
            self.block_label_timer.stop()
        elif reverse and self.block_label_alpha == 1:
            self.block_label_timer.stop()
            self.block_label.hide()

    def disable_toggle_buttons(self, toggle_buttons: tuple[ToggleButton:]) -> None:
        """Disables all the notification toggle buttons except for the disabling button"""
        for btn in toggle_buttons:
            if btn is self.sender():
                continue
            btn.set_ordinary()
            if self.sender().isChecked():
                btn.set_blocked_off(True)

    def remove_created_file(self, file_path: str, file_type: str) -> None:
        """Remove created file"""
        if os.path.exists(file_path):
            os.remove(file_path)
            self.log_record("{0} ({1}) was removed.".format(file_type, pathlib.Path(file_path).name), "info")  # Logging

    def copy_session_id(self) -> None:
        """Copy session ID"""
        pyperclip.copy(self.session_id)
        self.log_record(f"Session ID ({self.session_id}) was copied.", "info")  # Logging

    def copy_address(self) -> None:
        """Copy the address of a current toponym"""
        if self.json_data is None:
            self.play_audio(WARNING_SOUND)
            pop_up = WarningDialog("Coping address", "Search for a toponym before.", "icons/warning_icon_dialog.png")
            pop_up.exec()
            return

        # Logging
        self.log_record(f"Address ({self.toponym_address[:20] + '...' if len(self.toponym_address) > 23 else self.toponym_address}) was copied.", "info")
        pyperclip.copy(self.toponym_address)

    def copy_coordinates(self) -> None:
        """Copy coordinates of the current toponym"""
        if self.json_data is None:
            self.play_audio(WARNING_SOUND)
            pop_up = WarningDialog("Coping coordinates", "Search for a toponym before.",
                                   "icons/warning_icon_dialog.png")
            pop_up.exec()
            return

        # Logging
        self.log_record(f"Coordinates ({self.toponym_coords}) were copied.", "info")
        pyperclip.copy(self.toponym_coords)

    def copy_post_code(self) -> None:
        """Copy post code of the current toponym"""
        if self.json_data is None or self.toponym_postal_code is None:
            if self.json_data is None:
                message = "Search for a toponym before."
            elif self.toponym_postal_code is None:
                message = "No postal code found."

            self.play_audio(WARNING_SOUND)
            pop_up = WarningDialog("Coping postal code", message, "icons/warning_icon_dialog.png")
            pop_up.exec()
            return

        pyperclip.copy(self.toponym_postal_code)
        self.log_record(f"Postal code ({self.toponym_postal_code}) was copied.", "info")  # Logging

    def copy_mail(self) -> None:
        """Copies mail"""
        pyperclip.copy(self.label_mail.text())
        self.log_record("Mail address ({address}) was copied.".format(address=self.label_mail.text()), 'info')

    def play_audio(self, path: str) -> None:
        """Play audio files"""
        sounds = {WARNING_SOUND: self.play_warning_dialog_sound_tb.isChecked(),
                  INFORMATION_SOUND: self.play_information_dialog_sound_tb.isChecked(),
                  ERROR_SOUND: self.play_error_dialog_sound_tb.isChecked(),
                  OPEN_SOUND: self.play_open_application_sound_tb.isChecked(),
                  ACHIEVEMENT_SOUND: self.play_secret_achievement_sound_tb.isChecked()}

        if sounds.get(path, True):
            self.player.setMedia(QMediaContent(QUrl.fromLocalFile(path)))
            self.player.play()

    @property
    def random_address(self):
        longitude = round(random.uniform(-179.99, 179.99), 6)
        latitude = round(random.uniform(-89.99, 89.99), 6)

        request = self.request_get("http://geocode-maps.yandex.ru/1.x/",
                                   params={'apikey': GEOCODE_APIKEY,
                                           'format': 'json',
                                           'geocode': f"{longitude},{latitude}"}).json()

        objects = request['response']['GeoObjectCollection']['featureMember']
        return objects[0]['GeoObject']['metaDataProperty']['GeocoderMetaData']['text'] if objects else "Атлантический океан"

    def move_window(self, event) -> None:
        """Function making window able to be moved"""

        # Show the window normalized if it was maximized
        if self.isMaximized():
            self.resize_window()

        if event.buttons() == Qt.LeftButton:
            self.move(self.pos() + event.globalPos() - self.drag_postion)
            self.drag_postion = event.globalPos()
            event.accept()

    def set_selected_style(self) -> None:
        """Change the left-menu buttons style depends on active this or not"""
        cur_button = self.sender()
        cur_button_image = self.image_url_pattern.search(cur_button.styleSheet()).group(1)  # Image of the button
        cur_button.setStyleSheet(FOCUSED_BUTTON_STYLE.format(image=cur_button_image))

        all_buttons = [btn for btn in self.leftmenu_frame.children()
                       if isinstance(btn, QPushButton) and btn.objectName() != 'menu_button']

        # Changing all buttons (except for the pressed one) styles to ordinary
        for button in all_buttons:
            if button != cur_button:
                btn_image = self.image_url_pattern.search(button.styleSheet()).group(1)
                button.setStyleSheet(BUTTON_STYLE.format(image=btn_image))

    def pc_state_update(self) -> None:
        """Display information of current CPU state"""
        self.current_cpu_usage = psutil.cpu_percent() + 1
        self.current_ram_usage = psutil.virtual_memory().percent
        self.current_battery_charge = psutil.sensors_battery().percent

        # Renew the latest percentages of CPU
        self.latest_cpu_values.append(self.current_cpu_usage)
        if len(self.latest_cpu_values) > 7:
            self.latest_cpu_values = self.latest_cpu_values[-7:]

        # Renew the latest percentages of memory
        self.latest_ram_values.append(self.current_ram_usage)
        if len(self.latest_ram_values) > 7:
            self.latest_ram_values = self.latest_ram_values[-7:]

        # CPU current, highest, average, lowest values update
        self.cpu_bar.set_value(min(100, math.ceil(self.current_cpu_usage)))

        self.cpu_highest_value_progressbar.setValue(math.ceil(max(self.latest_cpu_values)))
        self.highest_cpu_value_label.setText(f"{math.ceil(max(self.latest_cpu_values))} %")

        self.cpu_average_value_progessbar.setValue(math.ceil(sum(self.latest_cpu_values) / len(self.latest_cpu_values)))
        self.average_cpu_value_label.setText(f"{math.ceil(sum(self.latest_cpu_values) / len(self.latest_cpu_values))} %")

        self.cpu_lowest_value_progressbar.setValue(math.ceil(min(self.latest_cpu_values)))
        self.lowest_cpu_value_label.setText(f"{math.ceil(min(self.latest_cpu_values))} %")

        # Memory current, highest, average, lowest values update
        self.ram_bar.set_value(min(100, math.ceil(self.current_ram_usage)))

        self.ram_lowest_value_progressbar.setValue(math.ceil(min(self.latest_ram_values)))
        self.lowest_ram_value_label.setText(f"{math.ceil(min(self.latest_ram_values))} %")

        self.ram_average_value_progessbar.setValue(math.ceil(sum(self.latest_ram_values) / len(self.latest_ram_values)))
        self.average_ram_value_label.setText(f"{math.ceil(sum(self.latest_ram_values) / len(self.latest_ram_values))} %")

        self.ram_highest_value_progressbar.setValue(math.ceil(max(self.latest_ram_values)))
        self.highest_ram_value_label.setText(f"{math.ceil(max(self.latest_ram_values))} %")

        # Max and min registered CPU usage values
        if math.ceil(self.current_cpu_usage) > int(''.join(filter(lambda c: c.isdigit(), self.max_cpu_usage_value.text()))):
            self.max_cpu_usage_value.setText(f"{math.ceil(self.current_cpu_usage)} %")
            self.max_cpu_usage_description.setText(f"({PERCENT_DESCRIPTIONS[math.ceil(self.current_cpu_usage) // 10]})")
        if math.ceil(self.current_cpu_usage) < int(''.join(filter(lambda c: c.isdigit(), self.min_cpu_usage_value.text()))):
            self.min_cpu_usage_value.setText(f"{math.ceil(self.current_cpu_usage)} %")
            self.min_cpu_usage_description.setText(f"({PERCENT_DESCRIPTIONS[math.ceil(self.current_cpu_usage) // 10]})")
            if math.ceil(self.current_cpu_usage) == 42:  # EASTER EGG !!!
                self.min_cpu_usage_description.setText("Answer...")

        # Max and min registered RAM usage values
        if math.ceil(self.current_ram_usage) > int(''.join(filter(lambda c: c.isdigit(), self.max_ram_usage_value.text()))):
            self.max_ram_usage_value.setText(f"{math.ceil(self.current_ram_usage)} %")
            self.max_ram_usage_description.setText(f"({PERCENT_DESCRIPTIONS[math.ceil(self.current_ram_usage) // 10]})")
        if math.ceil(self.current_ram_usage) < int(''.join(filter(lambda c: c.isdigit(), self.min_ram_usage_value.text()))):
            self.min_ram_usage_value.setText(f"{math.ceil(self.current_ram_usage)} %")
            self.min_ram_usage_description.setText(f"({PERCENT_DESCRIPTIONS[math.ceil(self.current_ram_usage) // 10]})")

    def check_pc_state(self) -> None:
        """Checks the state of pc every 750 msec"""
        if self.current_cpu_usage >= self.cpu_slider.value():
            if self.high_cpu_notification_tb.isChecked() and not self.disable_all_notification_tb.isChecked():
                if (dt.now() - self.delta_timer_cpu).total_seconds() >= 60:  # Shows the notification min. every 60 secs
                    self.notify("High CPU usage", f"Current usage: {min(round(self.current_cpu_usage), 100)}%",
                            (self.high_cpu_notification_tb.isChecked() and not self.disable_all_notification_tb.isChecked()))
                    self.delta_timer_cpu = dt.now()
        if self.current_ram_usage >= self.ram_slider.value():  # Shows the notification min. every 60 secs
            if self.high_memory_notification_tb.isChecked() and not self.disable_all_notification_tb.isChecked():
                if (dt.now() - self.delta_timer_ram).total_seconds() >= 60:
                    self.notify("High memory usage", f"Current usage: {min(round(self.current_ram_usage), 100)}%",
                                (self.high_memory_notification_tb.isChecked() and not self.disable_all_notification_tb.isChecked()))
                    self.delta_timer_ram = dt.now()
        if self.current_battery_charge <= self.battery_slider.value():  # Shows the notification min. every 60 secs
            if self.low_battery_notification_tb.isChecked() and not self.disable_all_notification_tb.isChecked():
                if (dt.now() - self.delta_timer_battery).total_seconds() >= 60:
                    self.notify("Low battery charge", f"Current charge: {self.current_battery_charge}%",
                                (self.low_battery_notification_tb.isChecked() and not self.disable_all_notification_tb.isChecked()))
                    self.delta_timer_battery = dt.now()

    def log_record(self, message: str, message_type: str) -> None:
        """Creates the data for log record and calls the logging function"""
        log_selectors = {"app_name": self.display_application_name_tb.isChecked(),
                         "computer_user": self.display_computer_username_tb.isChecked(),
                         "computer_name": self.display_computer_name_tb.isChecked(),
                         "date": self.display_recording_date_tb.isChecked(),
                         "time": self.display_recording_time_tb.isChecked(),
                         "session_id": self.display_session_id_tb.isChecked(),
                         "msg_lvl": self.display_message_log_level_tb.isChecked(),
                         "msg_name": self.display_message_log_name_tb.isChecked(),
                         "message": self.display_current_message_tb.isChecked()}

        extra = {"date": dt.now().strftime("%Y-%m-%d"),
                 "time": dt.now().strftime("%H:%M:%S"),
                 "msg_lvl": LOG_TYPE_TO_NUMBER[message_type.lower()],
                 "msg_name": LOG_TYPE_TO_NAME[message_type.lower()]}

        self.logger.message(message, message_type.lower(), log_selectors, extra_data=extra)

    def apply_log_settings(self) -> None:
        """Applies log settings"""
        message = None

        if not self.check_correct_input_records_number():
            phrases = {"Too large value": "Too large records number value.",
                       "Invalid value": "Invalid records number value."}
            message = phrases.get(self.records_number_error.text())

        if not self.check_correct_input_logfile():
            phrases = {"Invalid filepath": "Invalid log-file filepath"}
            message = phrases.get(self.log_error_label.text(), self.log_error_label.text()) + "."

        if not self.logFile_lineedit.text() or not self.rows_num_lineedit.text():
            message = "Empty input fields."

        if message is not None:
            self.play_audio(WARNING_SOUND)
            WarningDialog("Setting log-file", message, "icons/warning_icon_dialog.png").exec()
            return

        file_path = self.logFile_lineedit.text()
        file_name = pathlib.Path(file_path).name

        if pathlib.Path(file_path).exists():
            self.play_audio(INFORMATION_SOUND)
            pop_up = WarningDialog("Setting log-file",
                                   "Specified log-file will be rewritten.\nContinue?",
                                   "icons/info_icon_dialog.png", choice=True)
            pop_up.exec()
            if not pop_up.response:
                return

        # Creates log-file and clears the content
        if pathlib.Path(file_path).exists():
            os.chmod(file_path, stat.S_IWRITE)  # Avoid PermissionError if file is read only

        try:
            with open(file_path, mode='w', encoding=CODING) as log_file:
                log_file.write("")  # Explicit clear
            os.chmod(file_path, stat.S_IREAD)  # Make log-file read only
            self.log_record(f"Log-file ({file_path}) was created.", "info")
            self.notify(F"Log-file {file_name[:9] + '...' + file_name[-9:] if len(file_name) > 21 else file_name} was created.",
                        "CLick to open...",
                        (self.log_file_creating_notification_tb.isChecked() and not self.disable_all_notification_tb.isChecked()),
                        callback_on_click=lambda: os.startfile(file_path))
        except Exception as e:
            self.play_audio(ERROR_SOUND)
            WarningDialog("Setting log-file", f"{e.args[1]}.", "icons/error_icon_dialog.png").exec()

        # Writes the data to json-file
        write_json_data(filename=USER_JSON_DATA, indent=4, log_file=self.logFile_lineedit.text(),
                        records_number=int(self.rows_num_lineedit.text()))

        # Changes the logger properties
        self.logger.change_properties(filename=self.logFile_lineedit.text(),
                                      rows_count=int(self.rows_num_lineedit.text()))

    def reset_log_settings(self) -> None:
        """Resets log settings"""
        self.play_audio(INFORMATION_SOUND)
        pop_up = WarningDialog("Reset log settings", "Are you sure you want to reset log settings?",
                               "icons/info_icon_dialog.png", choice=True)
        pop_up.exec()

        if pop_up.response:
            write_json_data(filename=USER_JSON_DATA, indent=4, log_file=None, records_number=None)
            self.logFile_lineedit.setText("")
            self.rows_num_lineedit.setText("")
            self.information_msg_type_tb.setChecked(LOG_INFO_MESSAGE_TYPE)
            self.warning_msg_type_tb.setChecked(LOG_WARNING_MESSAGE_TYPE)
            self.error_msg_type_tb.setChecked(LOG_ERROR_MESSAGE_TYPE)
            self.display_computer_username_tb.setChecked(LOG_COMP_USER)
            self.display_application_name_tb.setChecked(LOG_APP_NAME)
            self.display_computer_name_tb.setChecked(LOG_COMP_NAME)
            self.display_recording_date_tb.setChecked(LOG_DATE)
            self.display_recording_time_tb.setChecked(LOG_TIME)
            self.display_session_id_tb.setChecked(LOG_SESSION_ID)
            self.display_message_log_level_tb.setChecked(LOG_MSG_LVL)
            self.display_message_log_name_tb.setChecked(LOG_MSG_NAME)
            self.display_current_message_tb.setChecked(LOG_MESSAGE)

    @staticmethod
    def show_time_here_dialog(time_here: int) -> None:
        """Shows the TimeHereDialog"""
        suffix = {'1': "st", '2': "nd", '3': "rd"}.get(str(time_here)[-1], 'th')
        TimeHereDialog(f"{time_here}{suffix}").exec()

    def follow_link(self, link: str) -> None:
        """Follow a website link"""
        wb.open(link)
        self.log_record(f'Followed ({link}) link.', "info")  # Logging
        self.notify(f"Followed: {link}", '{} official website.'.format(re.search(r"//(.+)\.\w{2,5}", link).group(1).lstrip('www.').lstrip('ru.').title()), True)

    def connect_warn(self) -> None:
        """Activates instead of raises ConnectionError of requests module"""
        self.play_audio(ERROR_SOUND)
        WarningDialog("Server requesting", "Connect to the Internet.", "icons/error_icon_dialog.png").exec()
        self.log_record(f"Internet connection error.", "error")

    def change_styles(self, button_group: dict) -> None:
        """Changes styles of buttons and its checkmarks"""
        cur_button = self.sender()
        cur_button.setStyleSheet(SELECTED_CHOICE_BUTTON_STYLE)

        # Styling buttons in the group
        for btn in button_group.keys():
            if btn != cur_button:
                btn.setStyleSheet(ORDINARY_CHOICE_BUTTON_STYLE)

        # Styling checkmark labels of buttons in the group
        for checkmark_btn in button_group.values():
            checkmark_btn.setIcon(QIcon(""))

        button_group[cur_button].setIcon(QIcon(r"icons\check_.png"))

    def show(self, is_being_opened=False):
        super().show()  # Call the super class .show method

        if is_being_opened is True:  # Show TimesHere dialog if the app is being opened only
            if self.current_times_here in TIMES_HERE:  # Play scene if amount of visits the application in TIMES_HERE
                self.block_label.show()
                self.block_label_timer.start(7)
                self.show_time_here_dialog(self.current_times_here)
                self.block_label_timer.timeout.disconnect()
                self.block_label_timer.timeout.connect(lambda: self.change_blocking_label_transparency(reverse=True))
                self.block_label_timer.start(7)

    def mousePressEvent(self, event) -> None:
        """Event activates when a mouse button getting pressed"""
        if self.track_buttons_to_stop_onestop:
            self.player.stop()
            self.track_buttons_to_stop_onestop = False

        self.drag_postion = event.globalPos()

    def keyPressEvent(self, event) -> None:
        if self.track_buttons_to_stop_onestop:
            self.player.stop()
            self.track_buttons_to_stop_onestop = False
        else:
            self.pressed_keys.append(keyevent_to_str(event, '+'))
            print(self.pressed_keys)
            if keyevent_to_str(event, '+').lower() == 'w':
                self.show_easter_egg()
            # if '.'.join(self.pressed_keys[-10:]).upper() in \
            #         ('w.w.s.s.a.d.a.d.b.a'.upper(), 'ц.ц.ы.ы.ф.в.ф.в.и.ф'.upper()):  # KONAMI CODE EASTER EGG
            #     self.show_easter_egg()

    def wheelEvent(self, ev) -> None:
        """Event activates when a mouse wheel getting scrolled"""

        # If search has not been started yet
        if self.longitude is None:
            return

        # If cursor in not on the image
        if not self.image.underMouse():
            return

        minimum_delta, delta = 1000, ev.angleDelta().y() // -120

        for value in MAP_SCALES:
            if abs(self.scale - value) < minimum_delta:
                index = MAP_SCALES.index(value)
                minimum_delta = abs(value - self.scale)

        new_scale = MAP_SCALES[index] * pow(2, delta)

        # Если увеличение выходит за границы, ее менять на границу соответствующего диапазона
        if (new_scale > MAP_SCALES[-1] and delta > 0) or (new_scale < MAP_SCALES[0] and delta < 0):
            return

        self.scale = new_scale

        # Запись в файл
        self.make_image(self.get_image(self.longitude, self.latitude, self.scale))
        self.image.setPixmap(QPixmap(FILE_IMAGE_NAME))

    def closeEvent(self, event) -> None:
        """Active when the main window being closed"""
        print(dir(event))
        if self.to_system_tray_tb.isChecked():  # If send the application to tray
            event.ignore()
            self.hide()

        app_log_settings_state = {btn.objectName(): btn.isChecked() for btn in self.log_toggle_buttons}
        app_system_behaviour_state = {btn.objectName(): btn.isChecked() for btn in self.system_behaviour_buttons}
        app_sound_state = {btn.objectName(): btn.isChecked() for btn in self.sounds_toggle_buttons}
        app_music_state = {self.music_slider.objectName(): self.music_slider.value()} | \
                          {btn.objectName(): btn.isChecked() for btn in self.music_toggle_buttons}
        app_notification_settings_state = {self.ram_slider.objectName(): self.ram_slider.value(),
                                           self.cpu_slider.objectName(): self.cpu_slider.value(),
                                           self.battery_slider.objectName(): self.battery_slider.value()} | \
                                          {btn.objectName(): btn.isChecked() for btn in self.notification_toggle_buttons}
        app_appearance_settings_state = {
            "dark_theme": self.appearance_theme_dark_button.styleSheet() == SELECTED_CHOICE_BUTTON_STYLE,
            "light_theme": self.appearance_theme_light_button.styleSheet() == SELECTED_CHOICE_BUTTON_STYLE
        } | {btn.objectName(): btn.isChecked() for btn in self.appearance_toggle_buttons}

        app_notification_type_settings_state = {
            "push_notification": self.notification_push_button.styleSheet() == SELECTED_CHOICE_BUTTON_STYLE,
            "app_notification": self.notification_app_button.styleSheet() == SELECTED_CHOICE_BUTTON_STYLE
        }

        # Writes the json-data of application state
        write_json_data(filename=APP_STATE_DATA, indent=4,
                        system_behaviour_settings=app_system_behaviour_state,
                        log_settings=app_log_settings_state,
                        appearance_settings=app_appearance_settings_state,
                        notification_type_settings=app_notification_type_settings_state,
                        notification_messages_settings=app_notification_settings_state,
                        sound_settings=app_sound_state,
                        music_settings=app_music_state)

        self.log_record("MapHelper is closed.", 'info')  # Logging

        if pathlib.Path(FILE_IMAGE_NAME).exists():
            os.remove(FILE_IMAGE_NAME)


if __name__ == '__main__':
    sys.excepthook = except_exceptions
    application = QApplication(sys.argv)
    QFontDatabase.addApplicationFont("fonts/open_sans_medium.ttf")
    QFontDatabase.addApplicationFont(f"fonts/open_sans_big.ttf")
    QFontDatabase.addApplicationFont("fonts/open_sans_regular.ttf")
    app = SplashScreen(MapHelper)
    app.show()  # app.show()
    sys.exit(application.exec())
