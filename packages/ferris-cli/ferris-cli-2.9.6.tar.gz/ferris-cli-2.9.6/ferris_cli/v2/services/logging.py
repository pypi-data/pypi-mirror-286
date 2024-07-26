import logging
import json
from logging import StreamHandler, Formatter

from .config import ApplicationConfigurator, DEFAULT_CONFIG
from .broker import FerrisBroker
from logstash_formatter import LogstashFormatterV1

LOGS_KEY = "ferris_cli.logging"
DEFAULT_TOPIC = 'ferris.logs'


class FerrisLogging:

    lg = None

    def get_logger(self, name, use_colors=False, _disable_streaming=False, _print_name=True):
        logging.raiseExceptions = False
        self.lg = logging.getLogger(name)

        self.lg.addHandler(
            FerrisLoggingHandler(use_colors=use_colors, _disable_streaming=_disable_streaming, _print_name=_print_name)
        )

        return self.lg

    def warning(self, msg):
        self.lg.warning(msg)

    def info(self, msg):
        self.lg.info(msg)

    def log(self, msg):
        self.lg.log(msg)

    def error(self, msg):
        self.lg.error(msg)

    def debug(self, msg):
        self.lg.debug(msg)

    def critical(self, msg):
        self.lg.critical(msg)

    def setLevel(self, level):
        self.lg.setLevel(level)


class FerrisLoggingHandler(StreamHandler):

    def __init__(self, topic=None, **kwargs):
        super().__init__()

        self.topic = topic or ApplicationConfigurator.get(DEFAULT_CONFIG).get('DEFAULT_LOGS_TOPIC', DEFAULT_TOPIC)
        self.use_colors = kwargs.get('use_colors', False)
        self._streaming_disabled = kwargs.get('_disable_streaming', False)
        self._print_name = kwargs.get('_print_name', True)

    def emit(self, record):
        self.setFormatter(CustomFormatter(self.use_colors, _print_name=self._print_name))
        super().emit(record)

        if not self._streaming_disabled:
            self.setFormatter(LogstashFormatterV1())
            msg = self.format(record)

            FerrisBroker().send(self.topic, json.loads(msg), True)


class CustomFormatter(Formatter):

    GREY = "\x1b[38;20m"
    YELLOW = "\x1b[33;20m"
    RED = "\x1b[31;20m"
    RED_BOLD = "\x1b[31;1m"
    CYAN = "\x1b[36;20m"
    GREEN = "\x1b[32;20m"

    RESET = "\x1b[0m"

    LOG_FORMAT = "%(asctime)s::%(name)s::%(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    LEVELS_LIST = {
        logging.DEBUG: GREEN,
        logging.INFO: CYAN,
        logging.WARNING: YELLOW,
        logging.ERROR: RED,
        logging.CRITICAL: RED_BOLD
    }

    formats = {}

    def __init__(self, use_colors=False, _print_name=True):
        super().__init__()

        if not _print_name:
            self.LOG_FORMAT = "%(asctime)s::%(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

        for level, color in self.LEVELS_LIST.items():
            self.formats[level] = f"{color if use_colors else ''}{self.LOG_FORMAT}{self.RESET if use_colors else ''}"

    def format(self, record):
        log_fmt = self.formats.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

