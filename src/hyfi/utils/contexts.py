import datetime
import os
from contextlib import contextmanager
from functools import partial
from timeit import default_timer

from hyfi.utils.funcs import FUNCs


def _elapser_timer(start):
    """A function that returns the elapsed time"""
    return default_timer() - start


def _elapser(start, end):
    """A function that returns the elapsed time"""
    return end - start


@contextmanager
def elapsed_timer(format_time=False):
    """A context manager that yields a function that returns the elapsed time"""
    start = default_timer()
    # elapser = lambda: default_timer() - start
    elapser = partial(_elapser_timer, start)
    yield lambda: str(
        datetime.timedelta(seconds=elapser())
    ) if format_time else elapser()
    end = default_timer()
    # elapser = lambda: end - start
    elapser = partial(_elapser, start, end)


@contextmanager
def change_directory(directory):
    """Change directory and change back to original directory"""
    original = os.path.abspath(os.getcwd())

    FUNCs.fancy_print(f" Change directory to {directory}")
    os.chdir(directory)
    try:
        yield

    except Exception as e:
        FUNCs.fancy_print(f" Exception: {e}")
        raise e

    finally:
        FUNCs.fancy_print(f" Change directory back to {original}")
        os.chdir(original)
