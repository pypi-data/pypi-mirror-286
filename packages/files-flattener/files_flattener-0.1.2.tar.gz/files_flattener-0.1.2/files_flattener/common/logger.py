import logging
import colorlog


class Logger:
    def __init__(self, name=__name__):
        self._logger_impl = logging.getLogger(name)
        self._logger_impl.setLevel(logging.DEBUG)

        # Create console handler and set level to debug
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # Create formatter with colors
        formatter = colorlog.ColoredFormatter(
            "%(log_color)s%(message)s",
            log_colors={
                "DEBUG": "green",
                "INFO": "white",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "red,bg_white",
            },
        )

        # Add formatter to ch
        ch.setFormatter(formatter)

        # Add ch to logger
        self._logger_impl.addHandler(ch)

    def debug(self, message):
        self._logger_impl.debug(message)

    def info(self, message):
        self._logger_impl.info(message)

    def warning(self, message):
        self._logger_impl.warning(message)

    def error(self, message):
        self._logger_impl.error(message)

    def critical(self, message):
        self._logger_impl.critical(message)


logger_instance = Logger()
