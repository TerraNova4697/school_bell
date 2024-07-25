import os
import logging
import asyncio

from boot import load_configurations
from exceptions import ConnectionLostException
from schoolbell import SchoolBell
from cron_manager import CronManager
from rest_client import CubaRestClient


logger = logging.getLogger("scheduler_logger")


async def run_server():
    try:
        # Load all constants.
        SCHOOL_BELL_TOKEN = os.environ.get("DEVICE_TOKEN")
        CUBA_URL = os.environ.get("CUBA_URL")
        CUBA_USER_EMAIL = os.environ.get("CUBA_USER_EMAIL")
        CUBA_USER_PASSWORD = os.environ.get("CUBA_USER_PASSWORD")
        USER = os.environ.get("USER")
        EXEC_SERVICE = os.environ.get("EXEC_SERVICE")
        EXEC_FILE = os.environ.get("EXEC_FILE")
        CONFIG_PATH = os.environ.get("CONFIG_PATH")

        # Load config on programm start.
        rest_client = CubaRestClient(
            CUBA_URL, CUBA_USER_EMAIL, CUBA_USER_PASSWORD, CONFIG_PATH
        )
        rest_client.get_device_attributes(device=SCHOOL_BELL_TOKEN)

        # Instantiate cron manager instance.
        cron_manager = CronManager(USER, EXEC_SERVICE, EXEC_FILE, CONFIG_PATH)

        # The main class of the brogramm. Connects to cuba and listens for attributes.
        school = SchoolBell(CUBA_URL, SCHOOL_BELL_TOKEN, cron_manager, CONFIG_PATH)
        school.connect()
        school.listen_attributes()
        school.listen_rpc()

        while True:
            await asyncio.sleep(1)

        raise ConnectionLostException(f"Connection to {CUBA_URL} lost.")

    except ConnectionError as e:
        logger.exception(e)
    except TimeoutError as e:
        logger.exception(e)

    finally:
        try:
            school.unsubscribe_from_all_attributes()
            school.disconnect()
        except UnboundLocalError:
            pass


if __name__ == "__main__":
    load_configurations()
    asyncio.run(run_server())
