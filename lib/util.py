import pickle
from loguru import logger


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
