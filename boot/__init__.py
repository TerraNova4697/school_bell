from dotenv import load_dotenv

from .argparser import parse_args
from .logging_manager import configure_logger


def load_configurations():
    args = parse_args()
    load_dotenv(override=True)
    configure_logger(args.mode)
