# -*- coding: utf-8 -*-
import logging
import socket
from logging.handlers import TimedRotatingFileHandler, RotatingFileHandler
from os.path import join

logging_hostname = socket.gethostname().split('.')[0]
SIMPLE_FORMAT = f'[%(asctime)s:{logging_hostname}:%(processName)s] %(levelname)s: %(message)s'
DEFAULT_FORMAT = f'[%(asctime)s:{logging_hostname}:%(processName)s:%(threadName)s] %(levelname)s: %(message)s'
VERBOSE_FORMAT = f'[%(asctime)s:{logging_hostname}:%(process)d:%(processName)s:%(thread)d:%(threadName)s] %(levelname)s: %(message)s'

PROCESS_DEFAULT_FORMAT = f'[%(asctime)s] Process(%(proc_id)s): %(message)s'
PROCESS_DEBUG_FORMAT = f'[%(asctime)s:{logging_hostname}:%(process)d:%(processName)s:%(thread)d:%(threadName)s] Process(%(proc_id)s): %(message)s'


def setup_logger(logger, debug_mode,
                 loglevel='INFO', logdir='./', logname='kompira',
                 stream=False, maxsz=0, backup=7, when='D',
                 formatter=None):
    lvl = getattr(logging, loglevel)
    fnm = join(logdir, logname + '.log')
    if debug_mode:
        hdl = logging.StreamHandler()
        lvl = logging.DEBUG
    elif stream:
        hdl = logging.StreamHandler()
    elif maxsz > 0:
        hdl = RotatingFileHandler(filename=fnm, maxBytes=maxsz,
                                  backupCount=backup)
    else:
        hdl = TimedRotatingFileHandler(filename=fnm, when=when,
                                       backupCount=backup)
    if any(isinstance(h, hdl.__class__) for h in logger.handlers):
        #
        # 同クラスのハンドラを二重登録しない
        #
        logger.warning("setup_logger('%s', %s, %s): %s has registered already", logger.name, debug_mode, loglevel, hdl.__class__.__name__)
    else:
        if not formatter:
            formatter = VERBOSE_FORMAT if debug_mode else DEFAULT_FORMAT
        fmt = logging.Formatter(formatter)
        hdl.setFormatter(fmt)
        hdl.setLevel(lvl)
        logger.addHandler(hdl)
    logger.setLevel(lvl)
