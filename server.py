import os
import sys

from config import CONFIG
from lib.tcp_server.service import Service
from lib.util import end_flush, is_flush, is_work
from lib.waveshare_epd import waveshare_epd
from PIL import Image
import socketserver
from loguru import logger
from progressbar import *
import click

from photo.photos import get_off_work

JPG = 'out.jpg'

logger.add('log/server/{time}.log', rotation='00:00')


class MyServer(Service):
    def flush(self):
        while True:
            if is_work():
                self.update()
            else:
                self.off_work()
                break
            self.connection_maintenance()

    def off_work(self):
        get_off_work()
        data = Image.open('%s' % JPG)
        epd = waveshare_epd.EPD(4.2)
        self.flush_buffer(epd.getbuffer(data))
        self.shutdown()

    def connection_maintenance(self):
        time.sleep(60)
        logger.success("剩余电量:" + str(self.check_batter()))

    def update(self):
        if is_flush():
            logger.info("发现画面更新，正在分发")
            data = Image.open('%s' % JPG)
            epd = waveshare_epd.EPD(4.2)
            self.flush_buffer(epd.getbuffer(data))
            end_flush()
        else:
            logger.info("未检测到画面更新")

    def handle(self):
        try:
            self.client = self.request
            self.get_id()
            self.unlock('123456')
            self.flush()
        except KeyboardInterrupt:
            self.shutdown()
            sys.exit()


@click.command()
@click.option('--profiles', default='home')
def run(profiles):
    logger.info('监听IP:{0} , 配置环境：{1}'.format(CONFIG[profiles]['host_ip'], profiles))
    socketserver.allow_reuse_address = True
    server = socketserver.ThreadingTCPServer((CONFIG[profiles]['host_ip'], 6868,), MyServer)
    server.serve_forever()


if __name__ == "__main__":
    run()
