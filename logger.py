import os.path

from core import *
from settings import *


class _MISSING_ARG:
    pass


class Logger:
    def __init__(self, filename: str, rows_count: int, encoding: str, info_on: bool, warning_on: bool, error_on: bool,
                 *, delimiter: str = ";", filemode: str = 'w', ignore_read_only: bool = True, **main_data) -> None:

        self.filename = filename
        self.rows_count = rows_count
        self.encoding = encoding
        self.delimiter = delimiter
        self.filemode = filemode
        self.ignore_read_only = ignore_read_only
        self.main_data = main_data

        self.info_on = info_on
        self.warning_on = warning_on
        self.error_on = error_on

    def message(self, message: str, message_type: str, format_filter: dict, *, extra_data: dict = None) -> None:
        """Writes the message to a file"""

        if not self.message_access.get(message_type, False):
            return

        if any(arg is None for arg in (self.filename, self.rows_count)):
            return

        if not os.path.exists(self.filename):
            return

        if extra_data is None:
            extra_data = dict()

        primary_data = {key: value.__str__() for (key, value) in (self.main_data | extra_data).items()}
        data = {key: value for (key, value) in primary_data.items() if format_filter.get(key, False)}
        ordered_data = {key: data.get(key) for key in MAIN_LOGGING_FORMAT if key in data} | {'message': message}
        cur_log = self.delimiter.join(ordered_data.values())

        if self.ignore_read_only:
            os.chmod(self.filename, stat.S_IWRITE)

        with open(self.filename, mode="rt", encoding=self.encoding) as file_to_read:
            read_data = list(map(lambda s: s.rstrip("\n"), file_to_read))

        data_to_write = "\n".join(read_data + [cur_log])
        # If numbers of the rows is greater than a specified maximum
        if len(read_data) >= self.rows_count:
            data_to_write = "\n".join(read_data[1:] + [cur_log])

        with open(self.filename, mode=self.filemode, encoding=self.encoding) as file:
            file.write(f"{data_to_write}\n")

        os.chmod(self.filename, stat.S_IREAD)

    def change_properties(self, *, filename: str = _MISSING_ARG(), rows_count: int = _MISSING_ARG(),
                          encoding: str = _MISSING_ARG(), info_on: bool = _MISSING_ARG(),
                          warning_on: bool = _MISSING_ARG(), error_on: bool = _MISSING_ARG(),
                          delimiter: str = _MISSING_ARG(), filemode: str = _MISSING_ARG(),
                          ignore_read_only: bool = _MISSING_ARG()) -> None:
        """Changes properties and settings of logging"""

        if not isinstance(filename, _MISSING_ARG):
            self.filename = filename
        if not isinstance(rows_count, _MISSING_ARG):
            self.rows_count = rows_count
        if not isinstance(encoding, _MISSING_ARG):
            self.encoding = encoding
        if not isinstance(info_on, _MISSING_ARG):
            self.info_on = info_on
        if not isinstance(warning_on, _MISSING_ARG):
            self.warning_on = warning_on
        if not isinstance(error_on, _MISSING_ARG):
            self.error_on = error_on
        if not isinstance(delimiter, _MISSING_ARG):
            self.delimiter = delimiter
        if not isinstance(filemode, _MISSING_ARG):
            self.filemode = filemode
        if not isinstance(ignore_read_only, _MISSING_ARG):
            self.ignore_read_only = ignore_read_only

    @property
    def message_access(self) -> dict:
        return {"info": self.info_on, "warning": self.warning_on, "error": self.error_on}

    def __repr__(self):
        return f"{type(self).__qualname__}({self.filename=}, {self.rows_count=}, {self.encoding=}, " \
               f"{self.info_on=}, {self.warning_on=}, {self.delimiter=}, {self.filemode=}, {self.ignore_read_only=})"
