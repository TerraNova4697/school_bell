import logging
import argparse
import os
import json

from datetime import datetime

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
        "--type",
        type=str,
        help="Variants: start / end",
        choices=["start", "end"],
    )
    parser.add_argument_group("required arguments").add_argument(
        "--shift",
        type=int,
        help="Variants: 1 / 2",
        choices=[1, 2],
    )
    parser.add_argument_group("required arguments").add_argument(
        "--lesson",
        type=int,
        help="Number of lesson",
    )

    return parser.parse_args()


def allowed_to_run_bell(config, shift, lesson) -> bool:
    now_timestamp = int(datetime.now().timestamp()) * 1000
    if config[f"shift{shift}LessonsNum"] < lesson:
        return False

    fire = int(_redis.get("fire").decode())
    alarm = int(_redis.get("alarm").decode())

    if not fire and not alarm:
        # print(f"{not config['isOff']} and {config['offTill'] < now_timestamp}")
        # print(f"{config['isOff']} and {config['onTill'] > now_timestamp}")
        # print(f"{now_timestamp} | {config['offTill']} | {config['onTill']}")

        if config["isOnFor"][0] < now_timestamp < config["isOnFor"][1]:
            return True
        if (
            not config["isOff"]
            and not config["isOffFor"][0] < now_timestamp < config["isOffFor"][1]
        ):
            return True
        # if not config["isOff"] and config["offTill"] < now_timestamp:
        #     return True
        # if config["isOff"] and config["onTill"] > now_timestamp:
        #     return True

    return False


def run(type_of_file, infinite=False):
    print(f"running bell for lesson {type_of_file}")
    p.stop_sound()
    if infinite:
        print("Starting infinite sound")
        p.start_infinite_sound(type_of_file)
    else:

        print("Starting finite sound", datetime.now())
        p.start_sound(type_of_file)


def run_priority(alarm_type):
    CONFIG_PATH = os.environ.get("CONFIG_PATH")

    with open(CONFIG_PATH, "r") as config_file:
        config = json.load(config_file)
        file = config[f"{alarm_type}Path"]

        run(file, infinite=True)


def stop_priority():
    # TODO: Stop all priority running files
    logger.info("Stopping all priority files.")
    p.stop_sound()


def main(type_of_file: str, shift: int, lesson: int):
    CONFIG_PATH = os.environ.get(
        "CONFIG_PATH",
        default=str(os.path.dirname(os.path.abspath(__file__)) + "/config.json"),
    )

    # logger.info(f"CONFIG_PATH {CONFIG_PATH}")
    print(f"CONFIG_PATH {CONFIG_PATH}")

    with open(CONFIG_PATH, "r") as config_file:
        config = json.load(config_file)
        if allowed_to_run_bell(config, shift, lesson):
            logger.warning("run script.")
            file = (
                config["startLessonPath"]
                if type_of_file == "start"
                else config["endLessonPath"]
            )
            run(file)
        else:
            logger.warning("Do not run script. It may be due to alarm.")


if __name__ == "__main__":
    args = parse_args()
    main(args.type, args.shift, args.lesson)
