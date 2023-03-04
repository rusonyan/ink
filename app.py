import random
import time

from loguru import logger

from config import CONFIG
from lib.util import write_new_pic
from meet import meets, my_meet
from weather import weathers

logger.add('log/app/{time}.log', rotation='00:00')

OPERATION_FUN = [weathers.handle, meets.handle, my_meet.handle]


def run():
    while True:
        logger.success("开始爬取数据")
        OPERATION_FUN[random.randint(0, len(OPERATION_FUN) - 1)]()
        write_new_pic()
        logger.success("画面准备完毕")
        time.sleep(CONFIG['sleep_time'])


if __name__ == '__main__':
    run()
