import os
import random
import shutil

PHOTO_ALBUM = ['card.jpg', 'lp.jpg', 'swx.jpg']


def handle():
    shutil.copy(os.path.join(os.getcwd(), 'static', 'photo', PHOTO_ALBUM[random.randint(0, len(PHOTO_ALBUM) - 1)]),
                os.getcwd() + '\\out.jpg')


if __name__ == "__main__":
    handle()
