import logging as log
from collections import defaultdict
from functools import partial
from time import monotonic

from tabulate import tabulate


"""
Measure static class.
Defaults to reports every 5 seconds.
"""
class Measure():
    data = defaultdict(dict)
    lastreport = None
    timeout = 5

    def __init__(self):
        pass

    """
    Timeout in seconds
    """
    @staticmethod
    def setInterval(timeout:int):
        Measure.timeout = timeout
        Measure.lastreport = monotonic()

    @staticmethod
    def measurer(index):
        return Measurer(index)

    @staticmethod
    def report():
        log.info("Measure report")
        rows = []
        rows += [['Index','Count','ms/exec','calls/sec']]
        for k, v in Measure.data.items():
            try:
                row = []
                row.append(k)
                row.append(v['count'])
                row.append(round(v['ms']/v['count'],3))
                try:
                    row.append(round(len(v['flares'])/(v['flares'][-1]-v['flares'][0]),3))
                except ZeroDivisionError:
                    row.append('-')

                rows.append(row)
            except KeyError:
                pass

        log.info(tabulate(rows))

    @staticmethod
    def report_if_time():
        if Measure.timeout is not None:
            if (monotonic() - Measure.lastreport) > Measure.timeout:
                Measure.report()
                Measure.lastreport = monotonic()

    @staticmethod
    def start(index):
        Measure.report_if_time()

        mi = Measure.data[index]
        if 'count' not in mi:
            mi['count'] = 0
        mi['count'] += 1
        if 'flares' not in mi:
            mi['flares'] = []
        mi['flares'].append(monotonic())
        while monotonic() - mi['flares'][0] > 15:
            mi['flares'].pop(0)
        mi['last'] = monotonic()

    @staticmethod
    def stop(index):
        if 'ms' not in Measure.data[index]:
            Measure.data[index]['ms'] = 0

        Measure.data[index]['ms'] += (monotonic() - Measure.data[index]['last'])*1000.0
        del Measure.data[index]['last']
        Measure.report_if_time()



class Measurer():
    """
    Use as a context manager to measure. It's a very light layer on the Measure static object.
        with Measurer('socalledfastdenoise'):
            for x in range(1000):
                socalled_fast_denoise()

    """
    def __init__(self, index):
        self.start = partial(Measure.start, index=index)
        self.stop = partial(Measure.stop, index=index)

    def __enter__(self):
        self.start()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
