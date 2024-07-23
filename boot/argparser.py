import argparse


def parse_args() -> argparse.Namespace:
    """Parse arguments from command line.

    Returns:
        argparse.Namespace: Namespace of passed arguments
    """
    parser = argparse.ArgumentParser(
        description="Crontab manager for school schedule.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument_group("required arguments").add_argument(
        "--mode",
        type=int,
        help="0 - debug, 1 - development, 2 - production, 3 - silent",
        default=1,
    )

    return parser.parse_args()
