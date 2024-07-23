"""Here stored all configuration classes for the programm."""

from dataclasses import dataclass
import logging


@dataclass
class Log:
    logfiles = ["log/debug.log", "log/development.log", "log/production.log"]
    levels = [logging.DEBUG, logging.INFO, logging.WARNING]
