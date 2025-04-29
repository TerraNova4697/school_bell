"""Here stored all configuration classes for the programm."""

from dataclasses import dataclass
import logging


@dataclass
class Log:
    logfiles = ["/var/log/school_bell/debug.log", "/var/log/school_bell/development.log", "/var/log/school_bell/production.log"]
    levels = [logging.DEBUG, logging.INFO, logging.WARNING]
