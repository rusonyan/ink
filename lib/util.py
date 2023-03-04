import pickle
from datetime import datetime, time

from loguru import logger


def is_work() -> bool:
    return time.fromisoformat('07:50:00') < time.fromisoformat(
        datetime.now().strftime('%H:%M:%S')) < time.fromisoformat('16:30:00')


def set_flag(s=True):
    with open('flag', 'wb') as f:
        pickle.dump(s, f)


def get_flag():
    with open('flag', 'rb') as f:
        result: bool = pickle.load(f)
        return result


def is_flush() -> bool:
    return get_flag()


def end_flush():
    set_flag(False)


def write_new_pic():
    set_flag(True)
