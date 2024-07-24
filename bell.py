import logging
import argparse
import os

from datetime import datetime


logger = logging.getLogger("scheduler_logger")


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

    return parser.parse_args()


def allowed_to_run_bell() -> bool:
    attrs = {}
    curr_dir = os.path.dirname(__file__)
    with open(curr_dir + "/attributes.txt") as attrs_file:
        lines = attrs_file.readlines()
        for line in lines:
            key, value = line.split("=")
            attrs[key] = int(value)

    return attrs["alarm"] == 0 and attrs["fire"] == 0


def run(type_of_file):
    logger.warning(f"running bell for lesson {type_of_file}")


def main(type_of_file: str):
    dt = datetime.now()
    if allowed_to_run_bell():
        run(type_of_file)
    else:
        logging.warning("Do not run script. It may be due to alarm.")
    logger.warning(f"running script for {type_of_file} of the lesson as {dt}")


if __name__ == "__main__":
    args = parse_args()
    main(args.type)
