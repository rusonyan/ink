import random
import time

from loguru import logger

from config import CONFIG
from lib.util import write_new_pic, is_work
from meet import meets, my_meet
from photo import photos
from weather import weathers

logger.add('log/app/{time}.log', rotation='00:00')

OPERATION_FUN = [
    # meets.handle,
    # weathers.handle,
    # meets.handle,
    # meets.handle,
    photos.handle
]


def sleep():
    logger.info("进入长时休眠")
    time.sleep(50400)


def run():
    while True:
        logger.success("开始更新数据")
        OPERATION_FUN[random.randint(0, len(OPERATION_FUN) - 1)]()
        write_new_pic()
        logger.success("画面准备完毕")
        time.sleep(CONFIG['sleep_time'])
        if not is_work():
            sleep()


if __name__ == '__main__':
    run()
