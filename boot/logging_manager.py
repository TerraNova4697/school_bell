import logging

from config import Log


def configure_logger(mode: int) -> None:
    """Configurate logger for the whole programm.

    Args:
        mode (int): Mode. Can be silent, debug, development and production.
    """
    if mode == 3:
        return

    logger = logging.getLogger("scheduler_logger")

    file_handler = logging.FileHandler(
        filename=Log.logfiles[mode], mode="a", encoding="utf-8"
    )
    file_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(filename)s - %(lineno)s - %(message)s"
        )
    )
    logger.addHandler(file_handler)
    logger.setLevel(Log.levels[mode])
