import logging
import argparse
import os
import json
import asyncio

from player import Player

import redis


logger = logging.getLogger("scheduler_logger")
p = Player()

_redis = redis.Redis(db=0)


def parse_args():
    """Parse arguments from command line.

    Returns:
        argparse.Namespace: Namespace of passed arguments
    """
    parser = argparse.ArgumentParser(
        description="Script for running bell.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument_group("required arguments").add_argument(
        "--alarm",
        type=str,
        help="Variants: alarm / fire / ambulance",
        choices=["alarm", "fire", "ambulance", "test"],
    )

    return parser.parse_args()


async def monitor_status():
    while True:
        fire = int(_redis.get("fire").decode())
        alarm = int(_redis.get("alarm").decode())
        test = int(_redis.get("test").decode())
        if not alarm and not fire and not test:
            p.stop_sound()
            exit()
        else:
            await asyncio.sleep(0.5)


async def main(type_of_alarm):
    asyncio.create_task(monitor_status())

    with open(
        os.path.dirname(os.path.abspath(__file__)) + "/config.json", "r"
    ) as config_file:
        config = json.load(config_file)
        file = config[f"{type_of_alarm}Path"]

        await p.start_infinite_sound(path=file)


if __name__ == "__main__":
    try:
        args = parse_args()
        asyncio.run(main(args.alarm))
    except Exception as e:
        logger.exception(e)
        print(e)
    finally:
        exit()
