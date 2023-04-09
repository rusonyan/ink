import os
import random
import shutil
from loguru import logger

PHOTO_ALBUM = ['lp.jpg']


def handle():
    photo_page = PHOTO_ALBUM[random.randint(0, len(PHOTO_ALBUM) - 1)]
    logger.success('即将展示{}'.format(photo_page))
    shutil.copy(os.path.join(os.getcwd(), 'static', 'photo', photo_page),
                os.path.join(os.getcwd(), 'out.jpg'))


def get_off_work():
    logger.success('下班页面推送')
    shutil.copy(os.path.join(os.getcwd(), 'static', 'photo', 'xiaban.jpg'),
                os.path.join(os.getcwd(), 'out.jpg'))


if __name__ == "__main__":
    handle()
