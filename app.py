import random
import time

from loguru import logger

from lib.util import write_new_pic
from meet import meet
from weather import weather

logger.add('log/app/{time}.log', rotation='00:00')

OPERATION_FUN = [weather.handle, meet.handle]


def run():
    while True:
        logger.success("开始爬取数据")
        OPERATION_FUN[random.randint(0, len(OPERATION_FUN)-1)]()
        write_new_pic()
        logger.success("画面准备完毕")
        time.sleep(600)


if __name__ == '__main__':
    run()
