#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
import sys

picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

# import
from PIL import Image

from waveshare_epd import waveshare_epd
from tcp_server import tcp_sver
import socketserver
import logging

from progressbar import *

logging.basicConfig(level=logging.INFO)


class MyServer(tcp_sver.tcp_sver):
    def handle(self):
        try:
            self.client = self.request
            self.Get_ID()
            self.unlock('123456')
            epd = waveshare_epd.EPD(4.2)
            self.set_size(epd.width, epd.height)
            x = 1
            # self.Shutdown()
            while True:
                data = Image.open('C:\\Users\\xiaomi\\PycharmProjects\\ink\\out.jpg')
                self.flush_buffer(epd.getbuffer(data))
                self.Shutdown()
                time.sleep(60)
        except ConnectionResetError:
            self.Wait_write("lose connect.")
        except KeyboardInterrupt:
            self.close()
        except:
            self.Shutdown()


if __name__ == "__main__":
    ip = tcp_sver.get_host_ip()
    logging.info('{0}'.format(ip))
    socketserver.allow_reuse_address = True
    server = socketserver.ThreadingTCPServer(("192.168.137.1", 6868,), MyServer)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()
        os.system("clear")
