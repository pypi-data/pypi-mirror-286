import inspect
import logging
import os
import sys
from datetime import datetime
from logging import handlers

import colorlog


class Logger:
    def __init__(self, level, save_path):
        self.save_path = save_path
        if self.save_path is not None:
            save = True
            os.makedirs(self.save_path, exist_ok=True)
        else:
            save = False
        caller_frame = inspect.stack()[2]
        caller_filename = os.path.splitext(os.path.basename(caller_frame.filename))[0]
        self.settings = {
            "LEVEL": self.lookup_table(level),
            "FILENAME": caller_filename,
            "MAYBYTES": 15 * 1024 * 1024,
            "BACKUPCOUNT": 100,
            "FORMAT": "%(log_color)s[%(levelname)-8s]%(reset)s [%(name)s]: %(module)s:%(lineno)d:  %(message)s",
            "SAVE": save,
        }
        self.logger_initialize()

    def lookup_table(self, idx):
        lvl = {
            "DEBUG": logging.DEBUG,
            "INFO": logging.INFO,
            "WARNING": logging.WARNING,
            "ERROR": logging.ERROR,
            "CRITICAL": logging.CRITICAL,
        }

        return lvl.get(idx, "INFO")

    def logger_initialize(self):
        self.logger = colorlog.getLogger(self.settings["FILENAME"])
        self.logger.setLevel(self.settings["LEVEL"])
        if len(self.logger.handlers) > 0:
            return self.logger
        stream_formatter = colorlog.ColoredFormatter(self.settings["FORMAT"])
        stream_handler = colorlog.StreamHandler(sys.stdout)
        now_date_time = "{:%Y-%m-%d}".format(datetime.now())
        stream_handler.setFormatter(stream_formatter)
        self.logger.addHandler(stream_handler)
        if self.settings["SAVE"]:
            file_formatter = logging.Formatter(
                "%(asctime)s [%(levelname)-8s] [%(name)s]: %(module)s:%(lineno)d: %(message)s"
            )
            file_handler = handlers.TimedRotatingFileHandler(
                os.path.abspath(f"{self.save_path}/{now_date_time}-{self.settings['FILENAME']}.log"),
                when="midnight",
                interval=1,
                backupCount=self.settings["BACKUPCOUNT"],
                encoding="utf-8",
            )
            file_handler.setFormatter(file_formatter)
            self.logger.addHandler(file_handler)


def logger_decorator(level, save_path=None):
    def decorator(obj):
        logger_instance = Logger(level, save_path).logger

        if isinstance(obj, type):  # Class decorator
            obj.logger = logger_instance
            original_init = obj.__init__

            def new_init(self, *args, **kwargs):
                original_init(self, *args, **kwargs)
                self.logger = logger_instance

            obj.__init__ = new_init
            return obj
        else:  # Function decorator

            def wrapper(*args, **kwargs):
                return obj(logger_instance, *args, **kwargs)

            return wrapper

    return decorator


@logger_decorator(level="DEBUG", save_path="logs")
class test:
    def __init__(self):
        self.logger.info("2")


if __name__ == "__main__":
    testssss = test()
    config = {
        "logger": {
            "level": "DEBUG",
            "save_path": "logs",
        }
    }
    log = Logger(config=config)
    logger = log.logger
    logger.debug("debug")
    logger.info("info")
    logger.warning("warning")
    logger.error("error")
    logger.critical("critical")
