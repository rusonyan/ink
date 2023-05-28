import logging
import math
import os
import socketserver
import struct
import time

from loguru import logger

pbar_cnt = 0


def progresses(id, date):
    if date == 0:
        logger.info('-----{0} 正在分发 0%  -----'.format(id))
    logger.info('-----{0} 正在分发 {1}%  -----'.format(id, date))
    if date == 100:
        logger.info('-----{0} 分发完毕 100%  -----'.format(id))


class Service(socketserver.BaseRequestHandler):
    ID = 'ruson'
    client = None
    width = 400
    height = 300
    b_width = math.ceil(400 / 8)
    length = 1024
    size = b_width * 300

    def get_msg(self):
        msg = b''
        temp = ''
        while temp != b'$':
            temp = self.client.recv(1)
            time.sleep(0.001)
        temp = self.client.recv(1)
        if temp != b'$':
            msg = msg + temp
        while True:
            temp = self.client.recv(1)
            if temp == b'#':
                break
            msg = msg + temp
        if msg == b'':
            msg = b'$'
        return msg

    def check_get(self, check=b'1'):
        msg = self.get_msg()
        if msg == check:
            return True
        else:
            return False

    def safe_send(self, send_msg, check):
        while True:
            self.client.sendall(send_msg)
            if self.check_get(check):
                break
            time.sleep(1)

    def send_cmd(self, cmd):
        check = 0
        cmd = cmd.encode()
        for i in range(0, len(cmd)):
            check = check ^ cmd[i]
        check = struct.pack(">B", check)
        cmd = b';' + cmd + b'/' + check
        self.safe_send(cmd, check)

    def send_data(self, data):
        check = 0
        for i in range(0, len(data)):
            check = check ^ data[i]
        data = [0x57] + data + [check]
        data = struct.pack(">%dB" % (len(data)), *data)
        check = struct.pack(">B", check)
        self.safe_send(data, check)

    def get_id(self):
        self.send_cmd('G')
        self.ID = self.get_msg().decode()
        logger.info("{} 已连接", self.ID)
        return self.ID

    def sleep_time(self, time):
        if time > 9999:
            time = 9999
            logging.debug("sleep time should be less than 9999 ")
        sleep_time = 'r' + str(time)
        self.send_cmd(sleep_time)

    def shutdown(self):
        self.send_cmd('S')
        logger.info("已关机")

    def reboot(self):
        self.send_cmd('R')

    def unlock(self, password):
        self.send_cmd('C')
        if self.get_msg() == b'1':
            logging.debug("lock")
            self.send_cmd('N' + password)
            if self.get_msg() == b'1':
                logging.debug("unlock")
        else:
            logging.debug("unlock")

    def check_batter(self):
        self.send_cmd('b')
        return int(self.get_msg()) * 3

    def clear(self):
        id = "id:{0} batter:{1}".format(self.ID, self.check_batter())
        self.send_cmd('F')
        global pbar_cnt
        cnnt = 20
        if pbar_cnt < cnnt:
            pbar_cnt = pbar_cnt + 1
        else:
            pbar_cnt = 1
        for i in range(0, math.ceil(self.size / self.length)):
            leng = self.length
            addr = i * leng
            num = (addr % 4096) // leng
            data = struct.pack(">IIB", addr, leng, num)
            data = struct.unpack(">9B", data)
            data = list(data)
            for j in range(0, leng):
                data = data + [0xff]
            self.send_data(data)
            pbar_num = int((i / math.ceil(self.size / self.length)) * 100)
            progresses(id, pbar_num)
        data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.send_data(data)
        self.send_cmd('D')
        progresses(id, 100)

    def flush_buffer(self, DATA):
        id = "id:{0} batter:{1}".format(self.ID, self.check_batter())
        time.sleep(0.1)
        self.send_cmd('F')
        for i in range(0, math.ceil(self.size / self.length)):
            leng = self.length
            addr = i * leng
            num = (addr % 4096) // leng
            data = struct.pack(">IIB", addr, leng, num)
            data = struct.unpack(">9B", data)
            data = list(data)
            for j in range(0, leng):
                if (i * leng + j) < len(DATA):
                    data = data + [DATA[j + i * leng]]
                else:
                    data = data + [0xFF]
            pbar_num = int((i / math.ceil(self.size / self.length)) * 100)
            progresses(id, pbar_num)
            self.send_data(data)
        data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.send_data(data)
        self.send_cmd('D')
        logger.info("画面刷新完毕")

    def handle(self):
        pass
