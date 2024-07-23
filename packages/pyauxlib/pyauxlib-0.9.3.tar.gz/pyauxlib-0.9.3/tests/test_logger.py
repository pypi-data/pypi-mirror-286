"""Test for the logger."""
import logging
import shutil
from collections.abc import Generator
from pathlib import Path
from typing import Any

import pytest
from pyauxlib.utils.logger import _set_level, init_logger

LOGS_PATH = Path("test_logs")


def test_set_level() -> None:
    """Test the _set_level function with various inputs.

    This test checks if the _set_level function correctly handles
    different types of input and raises appropriate exceptions
    for invalid inputs.
    """
    assert _set_level("DEBUG") == logging.DEBUG
    assert _set_level("debug") == logging.DEBUG
    assert _set_level(logging.INFO) == logging.INFO
    assert _set_level(None, default_level="ERROR") == logging.ERROR

    with pytest.raises(ValueError):
        _set_level("INVALID_LEVEL")

    # with pytest.raises(TypeError): # ??? Typeguard doesn't allow this test
    #     _set_level([])


def test_init_logger() -> None:
    """Test the init_logger function with different configurations.

    This test verifies that the init_logger function correctly
    sets up loggers with various configurations, including
    different log levels and output options.
    """
    # Test without output file
    logger = init_logger("test_logger", "DEBUG")
    assert logger.name == "test_logger"
    assert logger.level == logging.DEBUG
    assert any(isinstance(handler, logging.StreamHandler) for handler in logger.handlers)
    assert not any(isinstance(handler, logging.FileHandler) for handler in logger.handlers)

    # Test with output file
    logger = init_logger("test_logger_file", "DEBUG", output_folder=LOGS_PATH)
    assert logger.name == "test_logger_file"
    assert logger.level == logging.DEBUG
    assert any(isinstance(handler, logging.StreamHandler) for handler in logger.handlers)
    assert any(
        isinstance(handler, logging.handlers.RotatingFileHandler) for handler in logger.handlers
    )

    # Test with different console and file levels
    logger = init_logger(
        "test_logger_levels",
        "INFO",
        level_console="DEBUG",
        level_file="WARNING",
        output_folder=LOGS_PATH,
    )
    assert logger.level == logging.DEBUG  # The lowest level among all

    # Find handlers
    console_handler = None
    file_handler = None
    for handler in logger.handlers:
        if isinstance(handler, logging.StreamHandler) and not isinstance(
            handler, logging.FileHandler
        ):
            console_handler = handler
        elif isinstance(handler, logging.handlers.RotatingFileHandler):
            file_handler = handler

    assert console_handler is not None, "Console handler not found"
    assert file_handler is not None, "File handler not found"

    assert console_handler.level == logging.DEBUG
    assert file_handler.level == logging.WARNING

    # Clean up
    for handler in logger.handlers:
        handler.close()
        logger.removeHandler(handler)


def test_init_logger_file_output() -> None:
    """Test the file output of the logger.

    This test ensures that the logger correctly writes messages
    to the log file based on the specified log level.
    """
    logger = init_logger(
        "test_logger_file_output", "DEBUG", level_file="INFO", output_folder=LOGS_PATH
    )
    test_message = "This is a test message"
    logger.info(test_message)
    test_message_not_shown = "This won't be in the file"
    logger.debug(test_message_not_shown)

    # Close the handlers and get filenames
    filenames = []
    for handler in logger.handlers:
        if isinstance(handler, logging.FileHandler):
            filenames.append(handler.baseFilename)
        handler.close()
        logger.removeHandler(handler)

    # Check if the message is in the log file
    for filename in filenames:
        with Path(filename).open("r") as f:
            log_content = f.read()
        assert test_message in log_content
        assert test_message_not_shown not in log_content


def test_init_logger_console_output(capfd: Any) -> None:
    """Test the console output of the logger.

    Parameters
    ----------
    capfd : Any
        Pytest fixture to capture stdout/stderr

    This test verifies that the logger correctly outputs messages
    to the console based on the specified log level.
    """
    logger = init_logger("test_logger_console_output", "DEBUG", level_console="INFO")
    test_message = "This is a test message"
    logger.info(test_message)
    test_message_not_shown = "This won't be in the output"
    logger.debug(test_message_not_shown)

    # Capture the stdout and stderr output
    captured = capfd.readouterr()
    assert test_message in captured.out
    assert test_message_not_shown not in captured.out


def test_init_logger_color_output(capfd: Any) -> None:
    """Test the color output of the logger.

    Parameters
    ----------
    capfd : Any
        Pytest fixture to capture stdout/stderr

    This test ensures that the logger correctly applies color
    coding to different log levels in the console output when
    colored_console is True, and doesn't apply colors when it's False.
    """
    # Test with colored output
    logger = init_logger("test_logger_color", "DEBUG", colored_console=True)
    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")
    logger.critical("Critical message")

    captured = capfd.readouterr()
    assert "\033[0;36m" in captured.out  # Cyan for DEBUG
    assert "\033[0;32m" in captured.out  # Green for INFO
    assert "\033[0;33m" in captured.out  # Yellow for WARNING
    assert "\033[0;31m" in captured.out  # Red for ERROR
    assert "\033[0;35m" in captured.out  # Magenta for CRITICAL

    # Test without colored output
    logger = init_logger("test_logger_no_color", "DEBUG", colored_console=False)
    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")
    logger.critical("Critical message")

    captured = capfd.readouterr()
    assert "\033[0;36m" not in captured.out  # No Cyan for DEBUG
    assert "\033[0;32m" not in captured.out  # No Green for INFO
    assert "\033[0;33m" not in captured.out  # No Yellow for WARNING
    assert "\033[0;31m" not in captured.out  # No Red for ERROR
    assert "\033[0;35m" not in captured.out  # No Magenta for CRITICAL


@pytest.fixture(autouse=True)
def _cleanup() -> Generator[None, None, None]:
    """Fixture to clean up the log folder after each test.

    This fixture ensures that the log folder is cleaned up
    after each test, preventing interference between tests.

    Yields
    ------
    None
    """
    yield
    # Delete log folder for tests
    shutil.rmtree(LOGS_PATH, ignore_errors=True)
