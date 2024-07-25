import os, sys
from glob import glob, iglob

import math, cmath
import random

import re
from re import search, sub

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from random import shuffle
from time import sleep, time, monotonic
from functools import partial, reduce, cache
from itertools import tee, count, cycle, repeat, chain, pairwise
from statistics import mean, median, stdev
from pprint import pp
from collections import deque, defaultdict, namedtuple
import logging as log
import subprocess as sp
import threading as thread
import multiprocessing as multi

import json
import pickle

def file_datum(t=None, accuracy=False):
    """
    Usable file datum. T takes a datetime object. Accuracy boolean adds microseconds after a dot.

    :param t: datetime
    :param accuracy: bool
    :return: str
    """
    if t is None:
        t = datetime.now()
    datum = t.strftime("%Y%m%d_%H%M%S"+(".%f" if accuracy else ''))
    return datum

def from_datum(s):
    """
    Reverse of the file datum. Tries several formats and detects accuracy.

    :param s: file datum
    :return: datetime object
    """
    accuracy = bool(search('\.\d+$', s))
    options = [
        "%Y%m%d_%H%M%S" + (".%f" if accuracy else ''),
        "%Y%m%d %H%M%S" + (".%f" if accuracy else ''),
        "%Y/%m/%d %H/%M/%S" + (".%f" if accuracy else ''),
        "%Y/%m/%d %H/%M" + (".%f" if accuracy else '')]
    for x in options:
        try:
            obj = datetime.strptime(s, "%Y%m%d_%H%M%S"+(".%f" if accuracy else ''))
            return obj
        except Exception as ex:
            print(repr(ex))



def force_mkdir(path, critical=False):
    chain = []
    for x in path.split(os.sep):
        chain.append(x)
        force_mkdir_one(os.sep.join(chain), critical)


def force_mkdir_one(path, critical=False):
    """
    Catches the file exists error when trying to create a directory. Critical raises FileExistsError if the target is
    actually something else.

    :param path:
    :param critical: bool
    :raises FileExistError
    :return:
    """
    if os.path.exists(path) and not os.path.isdir(path):
        if critical:
            raise FileExistsError(f"{path} is not a directory when trying to create it.")
        else:
            log.debug(f"{path} is not a directory.")
            return
    if os.path.exists(path):
        return

    try:
        os.mkdir(path)
    except FileExistsError:
        pass

def hostname():
    """
    System hostname via sockets

    :return: str
    """
    import socket
    return socket.gethostname()