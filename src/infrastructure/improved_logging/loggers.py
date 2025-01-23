from typing import Optional

from src.infrastructure.improved_logging.main import LoggerReg, SetupLogger


class InitLoggers:
    main = LoggerReg(name="MAIN", level=LoggerReg.Level.INFO)
    cli = LoggerReg(name="CLI", level=LoggerReg.Level.INFO)
    executor = LoggerReg(name="EXECUTOR", level=LoggerReg.Level.INFO)
    models = LoggerReg(name="MODELS", level=LoggerReg.Level.INFO)
    yaml = LoggerReg(name="YAML", level=LoggerReg.Level.INFO)

    def __init__(self, debug: bool = False, set_level: Optional[LoggerReg.Level] = None) -> None:
        if debug:
            self.set_all_loggers_to_debug(level=set_level)

        SetupLogger(
            developer_mode=True,
            name_registration=[
                value
                for key, value in self.__class__.__dict__.items()
                if isinstance(value, LoggerReg)
            ],
        )

    def set_all_loggers_to_debug(self, level: Optional[LoggerReg.Level]) -> None:
        """Sets the logging level for all loggers."""
        for key, value in self.__class__.__dict__.items():
            if isinstance(value, LoggerReg):
                if level:
                    value.level = level
                else:
                    value.level = LoggerReg.Level.DEBUG


if __name__ == "__main__":
    test_logger = InitLoggers.main

    print(type(test_logger))    # <class 'src.infrastructure.logging.main.LoggerReg'>
    print(test_logger)          # LoggerReg(name='MAIN', level=<Level.DEBUG: 'DEBUG'>, propagate=False, write_file=False)

    test_logger_name = InitLoggers.main.name

    print(type(test_logger_name))   # <class 'str'>
    print(test_logger_name)         # MAIN
