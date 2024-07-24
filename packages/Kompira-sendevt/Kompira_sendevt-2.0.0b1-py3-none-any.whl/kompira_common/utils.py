# -*- coding: utf-8 -*-
import sys
import psutil
import tzlocal
from contextlib import contextmanager
from itertools import islice
from datetime import datetime
from multiprocessing.managers import SyncManager
from setproctitle import setproctitle, getproctitle


@contextmanager
def redirect_stdio(stdout, stderr):
    _stdout = sys.stdout
    _stderr = sys.stderr
    sys.stdout = stdout
    sys.stderr = stderr
    try:
        yield
    finally:
        sys.stdout = _stdout
        sys.stderr = _stderr


def system_timezone():
    """
    >>> system_timezone()
    'Asia/Tokyo'
    """
    return str(tzlocal.get_localzone())


def ignore_exception(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception:
        pass


def truncate_repr(data, length=64, end='...'):
    ext = '...' if len(data) > length else ''
    return repr(data[:length]) + ext


def truncate_join(iterable, limit=3, sep=', ', model='objects', end='...({} {})'):
    count = len(iterable)
    text = sep.join(str(o) for o in islice(iterable, limit))
    tail = end.format(count, model) if count > limit else ''
    return text + tail


def truncate_text(data, truncatechars=32):
    if isinstance(data, bytes):
        truncatechars //= 2
    tail = '...' if len(data) > truncatechars else ''
    data = data[:truncatechars]
    return repr(data) + tail


# cond 条件に合致する要素を inplace にリストから削除する
def remove_list(lst, cond, wipe=False):
    """
    >>> l = [(1, 'a'), (2, 'b'), (3, 'c'), (4, 'd')]
    >>> remove_list(l, lambda i, v: i in (1, 3))
    >>> l
    [(2, 'b'), (4, 'd')]

    >>> l = [(1, 'a'), (2, 'b'), (3, 'c'), (4, 'd')]
    >>> remove_list(l, lambda i, v: i in (1, 3), wipe=True)
    >>> l
    [(4, 'd')]

    >>> l = []
    >>> remove_list(l, lambda i, v: False)
    >>> l
    []
    """
    for idx, elem in reversed(list(enumerate(lst))):
        if cond(*elem):
            if wipe:
                del lst[0:idx+1]
                return
            del lst[idx]


class ProcTitleMixin:
    def settitle(self, title):
        name = getattr(self, 'name', self.__class__.__name__)
        setproctitle(f"{self.daemon_name}: [{name}] {title}")


class KompiraMPManager(SyncManager):
    @classmethod
    def _run_server(cls, *args, **kwargs):
        name = getproctitle().split(' ', 1)[0]
        setproctitle(f'{name} [MP-Manager]')
        return super()._run_server(*args, **kwargs)


_manager = None
def get_manager():
    global _manager
    if not isalive_mpmanager():
        _manager = KompiraMPManager()
        _manager.start()
    return _manager


def make_mpqueue(maxsize=0):
    manager = get_manager()
    return manager.Queue(maxsize)


def make_mpevent():
    manager = get_manager()
    return manager.Event()


def isalive_mpmanager():
    global _manager
    return _manager and _manager._process and _manager._process.is_alive()
