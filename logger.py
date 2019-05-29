import logging
import logging.handlers
import os
from datetime import datetime

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class FileLogger(object):
    __metaclass__ = Singleton

    CRITICAL = logging.CRITICAL
    ERROR = logging.ERROR
    WARNING = logging.WARNING
    INFO = logging.INFO
    DEBUG = logging.DEBUG
    NOTSET = logging.NOTSET

    def __init__(self, api_name, path_name, logging_level=20):
        self._api_name = api_name
        self._log_file_name = os.path.basename(path_name)
        self._path_name = os.path.dirname(path_name)
        self._logging_level = logging_level 

    def logger(self):
        try:
            logger = logging.getLogger(self._api_name)
            logger.setLevel(self._logging_level)
            absolute_log_path = self._path_name
            if not os.path.isdir(absolute_log_path):
                os.makedirs(absolute_log_path)
            file_handler = logging.FileHandler(os.path.join(absolute_log_path, self._log_file_name))
            file_handler.setLevel(self._logging_level)
            timestamp = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
            log_format = logging.Formatter(
                '[%(asctime)s - %(name)s - %(levelname)s - %(module)s - %(funcName)s() - %(lineno)d] - %(message)s',
                timestamp)
            file_handler.setFormatter(log_format)
            if not logger.handlers:
                logger.addHandler(file_handler)
            return logger
        except Exception as e:
            raise e
