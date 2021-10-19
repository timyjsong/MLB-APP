""" Custom logger for MLB-APP"""
# pylint: disable=too-few-public-methods, abstract-method

import logging
import sys


class DebugFormatter(logging.Formatter):
    """ Class for Debug Formatter"""

    def __init__(self):
        super().__init__("%(asctime)s  |  %(levelno)-2d  |  %(name)s  |  %(message)s")


class StdoutFormatter(logging.Formatter):
    """ Class for Stdout Formatter"""

    def __init__(self):
        super().__init__("%(message)s")


class StderrFormatter(logging.Formatter):
    """ Class for Stderr Formatter"""

    def __init__(self):
        super().__init__("[%(levelname)s] %(message)s")


class DebugFilter(logging.Filter):
    """ Class for Debug Filter"""

    def filter(self, record):
        """ filter function for Debug level"""

        return record.levelno


class StdoutFilter(logging.Filter):
    """ Class for Stdout Filter"""

    def filter(self, record):
        """ filter function for Stdout level"""

        return logging.INFO <= record.levelno < logging.WARNING


class StderrFilter(logging.Filter):
    """ Class for Stderr Filter"""

    def filter(self, record):
        """ filter function for Stderr level"""

        return record.levelno >= logging.WARNING


class DebugHandler(logging.FileHandler):
    """ Class for Debug Handler"""

    def __init__(self, logfile="debug.log"):
        super().__init__(logfile, mode="a")
        self.setFormatter(DebugFormatter())
        self.addFilter(DebugFilter())


class StdoutHandler(logging.StreamHandler):
    """ Class for Stdout Handler"""

    def __init__(self):
        super().__init__(sys.stdout)
        self.setFormatter(StdoutFormatter())
        self.addFilter(StdoutFilter())


class StderrHandler(logging.StreamHandler):
    """ Class for Stderr Handler"""

    def __init__(self):
        super().__init__(sys.stderr)
        self.setFormatter(StderrFormatter())
        self.addFilter(StderrFilter())


class Logger:
    """ Class for Logger"""

    level = 1
    running = False

    @classmethod
    def init_logger(cls):
        """ CLass Method for initiating logger"""

        cls.running = True

    def __init__(self, alias):
        self.alias = alias
        self.logger = logging.getLogger(alias)
        self.logger.setLevel(self.level)

        if not self.running:
            self.logger.addHandler(DebugHandler())
            self.logger.addHandler(StdoutHandler())
            self.logger.addHandler(StderrHandler())
            self.init_logger()

    def get_logger(self, alias):
        """ Recursive method that re-executes class init"""

        return Logger(".".join((self.alias, alias)))

    def debug(self, *args, **kwargs):
        """ overriding debug method"""

        self.logger.debug(*args, **kwargs)

    def info(self, *args, **kwargs):
        """ overriding info method"""

        self.logger.info(*args, **kwargs)

    def warning(self, *args, **kwargs):
        """ overriding warning method"""

        self.logger.warning(*args, **kwargs)

    def error(self, *args, **kwargs):
        """ overriding error method"""

        self.logger.error(*args, **kwargs)

    def critical(self, *args, **kwargs):
        """ overriding critical method"""

        self.logger.critical(*args, **kwargs)

    def exception(self, *args, **kwargs):
        """ overriding exception method"""

        self.logger.exception(*args, **kwargs)


LOGGER = Logger("MLB-APP")
LOGGER.debug("Initialized MLB-APP Logger Instance")
