#!/usr/bin/python
# -*- coding:utf-8 -*-

# *****************************************************************************
# * | File        :	  tcp_sver.py
# * | Author      :   Waveshare team
# * | Function    :   Electronic paper driver
# * | Info        :
# *----------------
# * | This version:   V1.0
# * | Date        :   2020/11/27
# # | Info        :   python demo
# -----------------------------------------------------------------------------
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documnetation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to  whom the Software is
# furished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS OR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#


#from tqdm import *
#from progressbar import *
import socketserver
import traceback
import threading
import binascii
import logging
import struct
import signal
import socket
from . import fcntl
import time
import math

pbar_cnt =0
#trange.pos = 0

def progresser(n,id,date):
  '''
  time.sleep(0.1)
  total = 100
  n_desc="{0}".format(id)
  trange.pos = 0  
  bar=trange(total,desc=n_desc,position=n,ascii=True,bar_format='{l_bar}{bar}')
  bar.update(date)
  if date==total:
    bar.close()
  '''
  if(date == 0):
        print('----- {0} progress is begin ----- \r\n'.format(id))
  print('\r {0} progress is {1}% \r\n'.format(id,date))
  if(date == 100):
        print('----- {0} progress is end ----- \r\n'.format(id),flush=True)
   
def get_host_ip():
    try:
        s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        s.connect(('8.8.8.8',80))
        ip=s.getsockname()[0]
    finally:
        s.close()
    return ip

class tcp_sver(socketserver.BaseRequestHandler):
    ID='nuknow'
    client=None
    size=0
    width=0
    hight=0
    b_width=0
    lenght=1024
    history_file_name ="History.txt"
    def set_size(self,w,h):
        self.width=w
        self.hight=h
        self.b_width=math.ceil(w/8)
        self.size=self.b_width*h
        
    def Wait_write(self,msg):
        with open(self.history_file_name, 'a') as f:
            fcntl.flock(f.fileno(), fcntl.LOCK_EX)
            now_time=time.strftime('%Y-%m-%d %H:%M:%S')
            f.write("time:{0}\tID:{1}\tIP:{2}\tPROT:{3}\t{4}\r\n".format(now_time,self.ID,self.client_address[0],self.client_address[1],msg))
            logging.debug("time:{0}\tID:{1}\tIP:{2}\tPROT:{3}\t{4}\r\n".format(now_time,self.ID,self.client_address[0],self.client_address[1],msg))
            fcntl.funlock(f.fileno())
            f.close()   
    def Get_msg(self):
        msg=b''
        temp=''
        while temp!=b'$':
            temp=self.client.recv(1)
            time.sleep(0.001)
        temp = self.client.recv(1)
        if temp!=b'$':
            msg=msg+temp
        while True:
            temp = self.client.recv(1)
            if temp==b'#':
                break
            msg=msg+temp
        if msg == b'':
            msg =b'$'
        return msg

    def check_get(self,check=b'1'):
        msg=self.Get_msg();
        if(msg==check):
            return True
        else :
            #print('get: {0} check:{1}'.format(msg,check))
            return False           

    def safe_send(self,send_msg,check):
        while True:
            self.client.sendall(send_msg)
            if(self.check_get(check)==True):
                break
            time.sleep(1)
             
    def Send_cmd(self,cmd): 
        check=0
        cmd=cmd.encode()
        
        for i in range(0,len(cmd)):
            check=check^cmd[i]
        check=struct.pack(">B",check)
        cmd=b';'+cmd+b'/'+check

        self.safe_send(cmd,check)
         
    def Send_data(self,data):
        check=0
        for i in range(0,len(data)):
            check=check^data[i]

        data=[0x57]+data+[check]
        data=struct.pack(">%dB"%(len(data)),*data) 
        check=struct.pack(">B",check)  
        self.safe_send(data,check)
        
    def Get_ID(self):   
        self.Send_cmd('G')
        self.ID=self.Get_msg().decode()
        self.Wait_write("connect.")
        return self.ID 
    def Sleep_time(self,time):
        if(time>9999):
            time=9999
            logging.debug("sleep time should be less than 9999 ")
        sleep_time='r'+str(time)
        self.Send_cmd(sleep_time)
    def Shutdown(self):
        self.Send_cmd('S')
    def Reboot(self):
        self.Send_cmd('R')      
    def unlock(self,password):
        self.Send_cmd('C')
        if (self.Get_msg()==b'1'):
            logging.debug("lock")
            self.Send_cmd('N'+password)
            if (self.Get_msg()==b'1'):
                logging.debug("unlock")
        else:
            logging.debug("unlock")
    def check_batter(self):
        self.Send_cmd('b') 
        return (int(self.Get_msg())*3)
    def clear(self):
        
        id="id:{0} batter:{1}".format(self.ID,self.check_batter())
        self.Send_cmd('F')
        global pbar_cnt
        cnnt =20
        if(pbar_cnt<cnnt):
            pbar_cnt=pbar_cnt+1
        else :
            pbar_cnt=1
            os.system("clear")
        pbar_cnt_loct=pbar_cnt
        #progresser(pbar_cnt_loct,id,0) 
        
        for i in range(0,math.ceil(self.size/self.lenght)):
            leng=self.lenght
            addr=i*leng         
            num=(addr%4096)//leng
            data=struct.pack(">IIB",addr,leng,num)
            data=struct.unpack(">9B",data)
            data=list(data)
            for j in range(0,leng):
                data=data+[0xff]
            self.Send_data(data)
            pbar_num=int((i/math.ceil(self.size/self.lenght))*100)
            progresser(pbar_cnt_loct,id,pbar_num)
        data=[0,0,0,0,0,0,0,0,0,0,0]
        self.Send_data(data)
        self.Send_cmd('D')
        progresser(pbar_cnt_loct,id,100)
    def flush_buffer(self,DATA):
        id="id:{0} batter:{1}".format(self.ID,self.check_batter())
        time.sleep(0.1)
        self.Send_cmd('F')
        global pbar_cnt
        cnnt =20
        if(pbar_cnt<cnnt):
            pbar_cnt=pbar_cnt+1
        else :
            pbar_cnt=1
            os.system("clear")
        pbar_cnt_loct=pbar_cnt
        #progresser(pbar_cnt_loct,id,0) 
        for i in range(0,math.ceil(self.size/self.lenght)):
            leng=self.lenght
            addr=i*leng         
            num=(addr%4096)//leng
            data=struct.pack(">IIB",addr,leng,num)
            data=struct.unpack(">9B",data)
            data=list(data)
            for j in range(0,leng):
                if (i*leng+j)<len(DATA):
                    data=data+[DATA[j+i*leng]]
                else:
                    data=data+[0xFF]
            
            pbar_num=int((i/math.ceil(self.size/self.lenght))*100)
            progresser(pbar_cnt_loct,id,pbar_num)
            self.Send_data(data)            
        data=[0,0,0,0,0,0,0,0,0,0,0]
        self.Send_data(data)
        self.Send_cmd('D') 
        self.Wait_write("Display over.")
        progresser(pbar_cnt_loct,id,100)

        
    def ota(self,ota_path):      
        self.Send_cmd('O')
        fsize = os.path.getsize(ota_path)
        logging.info("fsize={0}".format(fsize))
        file = open(ota_path,'rb')
        file.seek(0)
        pbar = ProgressBar().start()
        i=0
        starttime = time.time()
        for i in range(0,math.ceil(fsize/self.lenght)):      
            c= file.read(self.lenght)
            ssss = str(binascii.b2a_hex(c))[2:-1]
            self.client.sendall(bytes().fromhex(ssss))
            pbar.update(int(100*i*self.lenght/fsize))
            i=i+1
        file.close()  
        endtime = time.time()
        self.client.sendall(b'1')
        pbar.finish()  
        logging.info('OTA used time :{0}secs'.format(round(endtime - starttime, 2)))   
        time.sleep(2)
        self.Wait_write("OTA over.")
        
    def handle(self):
        pass