import logging
import argparse
import os
import json

from datetime import datetime

from player import Player


logger = logging.getLogger("scheduler_logger")
p = Player()


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
        "--schift",
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
    now_timestamp = datetime.now().timestamp()
    if config[f"shift{shift}LessonsNum"] < lesson:
        return False

    if not config["fire"] and not config["alarm"]:
        if not config["isOff"] and config["isOffTill"] < now_timestamp:
            return True
        if config["isOff"] and config["isOnTill"] > now_timestamp:
            return True

    return False


def run(type_of_file, infinite=False):
    logger.info(f"running bell for lesson {type_of_file}")
    p.stop_sound()
    if infinite:
        p.start_infinite_sound(type_of_file)
    else:
        p.start_sound(type_of_file)


def run_priority(alarm_type):
    CONFIG_PATH = os.environ.get("CONFIG_PATH")

    with open(CONFIG_PATH, "r") as config_file:
        config = json.load(config_file)
        file = config[f"{alarm_type}Path"]
        # TODO: Stop sound if playing.
        run(file, infinite=True)


def stop_priority():
    # TODO: Stop all priority running files
    logger.info("Stopping all priority files.")
    p.stop_sound()


def main(type_of_file: str, shift: int, lesson: int):
    CONFIG_PATH = os.environ.get("CONFIG_PATH")

    with open(CONFIG_PATH, "r") as config_file:
        config = json.load(config_file)
        if allowed_to_run_bell(config, shift, lesson):
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
