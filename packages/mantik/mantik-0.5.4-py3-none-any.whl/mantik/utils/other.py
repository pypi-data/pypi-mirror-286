import contextlib
import os


@contextlib.contextmanager
def temp_chdir(path: str):
    _old_cwd = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(_old_cwd)
