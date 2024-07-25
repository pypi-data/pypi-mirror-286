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

def force_mkdir(path):
    try:
        os.mkdir(path)
    except FileExistsError:
        pass

def hostname():
    import socket
    return socket.gethostname()