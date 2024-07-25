import logging as log
import os
from rotarysaw.colorlog import ColoredFormatter, FileFormatter

def init_log(name=None, file=True, level=log.DEBUG, color=True):
    root = log.getLogger(name=name)
    root.setLevel(level)
    if file:
        if isinstance(file, str):
            if file.index('.log') == -1:
                file += '.log'
            filename = file
        else:
            filename = f"{__name__}.log"

        try:
            os.mkdir('log')
        except FileExistsError:
            filename = 'log/'+filename
        except OSError:
            pass
        except PermissionError:
            pass
        else:
            filename = 'log/'+filename

        logfile = log.FileHandler(filename)
        if color:
            logfile.setFormatter(FileFormatter())
        root.addHandler(logfile)

    stream = log.StreamHandler()
    if color:
        stream.setFormatter(ColoredFormatter())
    root.addHandler(stream)