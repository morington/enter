from typing import Optional

from src.infrastructure.improved_logging.main import LoggerReg, SetupLogger


class InitLoggers:
    """
    A class to initialize and configure loggers for different components of the application.

    Attributes:
        main (LoggerReg): Logger for the main application.
        cli (LoggerReg): Logger for the command-line interface.
        executor (LoggerReg): Logger for the command executor.
        models (LoggerReg): Logger for the models.
        yaml (LoggerReg): Logger for YAML-related operations.

    Methods:
        __init__: Initializes loggers and optionally sets them to debug mode.
        set_all_loggers_to_debug: Sets the logging level for all loggers to debug or a specified level.
    """

    # Predefined loggers for different components
    main = LoggerReg(name="MAIN", level=LoggerReg.Level.INFO)
    cli = LoggerReg(name="CLI", level=LoggerReg.Level.INFO)
    executor = LoggerReg(name="EXECUTOR", level=LoggerReg.Level.INFO)
    models = LoggerReg(name="MODELS", level=LoggerReg.Level.INFO)
    yaml = LoggerReg(name="YAML", level=LoggerReg.Level.INFO)

    def __init__(self, debug: bool = False, set_level: Optional[LoggerReg.Level] = None) -> None:
        """
        Initializes loggers and optionally sets them to debug mode.

        Args:
            debug (bool, optional): If True, sets all loggers to debug mode. Defaults to False.
            set_level (Optional[LoggerReg.Level], optional): The logging level to set if debug is True. Defaults to None.
        """
        if debug:
            self.set_all_loggers_to_debug(level=set_level)

        # Initialize loggers with the specified configuration
        SetupLogger(
            developer_mode=True,
            name_registration=[
                value
                for key, value in self.__class__.__dict__.items()
                if isinstance(value, LoggerReg)
            ],
        )

    def set_all_loggers_to_debug(self, level: Optional[LoggerReg.Level]) -> None:
        """
        Sets the logging level for all loggers to debug or a specified level.

        Args:
            level (Optional[LoggerReg.Level]): The logging level to set. If None, sets to DEBUG.
        """
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
