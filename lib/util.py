import pickle
from datetime import datetime, time


def is_work():
    # return True
    return not time.fromisoformat(datetime.now().strftime('%H:%M:%S')) < time.fromisoformat('16:30:00')


def set_flag(s=True):
    with open('flag', 'wb') as f:
        pickle.dump(s, f)


def get_flag():
    with open('flag', 'rb') as f:
        result = pickle.load(f)
        return result


def is_flush():
    return get_flag()


def end_flush():
    set_flag(False)


def write_new_pic():
    set_flag(True)

set_flag(True)