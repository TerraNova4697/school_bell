import os
import logging
import asyncio

from boot import load_configurations
from exceptions import ConnectionLostException
from schoolbell import SchoolBell
from cron_manager import CronManager


logger = logging.getLogger("scheduler_logger")


async def run_server():
    try:
        SCHOOL_BELL_TOKEN = os.environ.get("DEVICE_TOKEN")
        CUBA_URL = os.environ.get("CUBA_URL")
        USER = os.environ.get("USER")
        EXEC_SERVICE = os.environ.get("EXEC_SERVICE")
        EXEC_FILE = os.environ.get("EXEC_FILE")

        cron_manager = CronManager(USER, EXEC_SERVICE, EXEC_FILE)

        school = SchoolBell(CUBA_URL, SCHOOL_BELL_TOKEN, cron_manager)
        school.connect()
        school.listen_rpc()

        while True:
            await asyncio.sleep(1)

        raise ConnectionLostException(f"Connection to {CUBA_URL} lost.")

    except ConnectionError as e:
        logger.exception(e)
    except TimeoutError as e:
        logger.exception(e)

    finally:
        school.disconnect()


if __name__ == "__main__":
    load_configurations()
    asyncio.run(run_server())
