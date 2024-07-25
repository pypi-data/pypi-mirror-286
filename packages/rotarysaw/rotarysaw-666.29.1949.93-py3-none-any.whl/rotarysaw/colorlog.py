# Ceph deploy, probably makes this licensed GPL

import logging
import sys
from pprint import pp, pformat


def insert(obj):

    if type(obj) in [str,int,float,bool]:
        return logging.info(obj)

    for line in pformat(obj).split("\n"):
        insert(line)
    return

logging.pp_info = insert


from datetime import datetime

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)
COLORS = { 'WARNING': YELLOW, 'INFO': WHITE, 'DEBUG': BLUE, 'CRITICAL': RED, 'ERROR': RED, 'FATAL': RED, }

RESET_SEQ = "\033[0m"
COLOR_SEQ = "\033[1;%dm"
BOLD_SEQ = "\033[1m"

BASE_COLOR_FORMAT = "[%(asctime)s][%(color_levelname)-4s] %(message)s"
BASE_FORMAT = "[%(asctime)s][%(name)s][%(levelname)-4s] %(message)s"

def color_message(message):
    message = message.replace("$RESET", RESET_SEQ).replace("$BOLD", BOLD_SEQ)
    return message

from time import strftime

class ColoredFormatter(logging.Formatter):
    """
    A very basic logging formatter that not only applies color to the levels of
    the ouput but will also truncate the level names so that they do not alter
    the visuals of logging when presented on the terminal.
    """

    def __init__(self):
        logging.Formatter.__init__(self, color_message(BASE_COLOR_FORMAT), datefmt='%H:%M:%S')

    def format(self, record):
        levelname = record.levelname
        truncated_level = record.levelname[:4]
        levelname_color = COLOR_SEQ % (30 + COLORS[levelname]) + truncated_level + RESET_SEQ
        record.color_levelname = levelname_color
        return logging.Formatter.format(self, record)

class FileFormatter(logging.Formatter):
    def __init__(self):
        logging.Formatter.__init__(self, color_message(BASE_FORMAT), datefmt="%H:%M:%S")

    def format(self, record):
        levelname = record.levelname
        truncated_level = record.levelname[:4]
        levelname_color = COLOR_SEQ % (30 + COLORS[levelname]) + truncated_level + RESET_SEQ
        record.color_levelname = levelname_color
        return logging.Formatter.format(self, record)
