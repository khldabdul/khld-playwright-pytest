"""Logging utilities for test automation framework."""

from __future__ import annotations

import logging
import sys
from pathlib import Path


def get_logger(
    name: str,
    level: int = logging.INFO,
    log_file: str | Path | None = None
) -> logging.Logger:
    """
    Get a configured logger instance.

    Args:
        name: Logger name (usually __name__)
        level: Logging level
        log_file: Optional file path for file logging

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)

    # Avoid adding handlers multiple times
    if logger.handlers:
        return logger

    logger.setLevel(level)

    # Console handler with formatting
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_format = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)

    # File handler if specified
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(log_path)
        file_handler.setLevel(level)
        file_format = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s (%(filename)s:%(lineno)d): %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(file_format)
        logger.addHandler(file_handler)

    return logger


def get_test_logger(test_name: str) -> logging.Logger:
    """
    Get a logger configured for a specific test.

    Args:
        test_name: Name of the test

    Returns:
        Logger instance
    """
    return get_logger(f"test.{test_name}")


class TestLogContext:
    """Context manager for test-specific logging."""

    def __init__(self, logger: logging.Logger, test_name: str):
        """
        Initialize TestLogContext.

        Args:
            logger: Logger instance
            test_name: Name of the test
        """
        self.logger = logger
        self.test_name = test_name

    def __enter__(self):
        """Start test logging context."""
        self.logger.info(f"Starting test: {self.test_name}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """End test logging context."""
        if exc_type is not None:
            self.logger.error(
                f"Test failed: {self.test_name} - {exc_type.__name__}: {exc_val}"
            )
        else:
            self.logger.info(f"Test passed: {self.test_name}")
        return False  # Don't suppress exceptions

    def step(self, description: str):
        """Log a test step."""
        self.logger.info(f"  Step: {description}")

    def debug(self, message: str):
        """Log debug information."""
        self.logger.debug(message)

    def warning(self, message: str):
        """Log a warning."""
        self.logger.warning(message)
