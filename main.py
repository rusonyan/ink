import datetime
import os
from datetime import datetime, time

import requests
from PIL import ImageFont, Image, ImageDraw
from bs4 import BeautifulSoup



def normal_out(left_top_point=30):
    start_time=time.fromisoformat('07:50:00')
    end_time=time.fromisoformat('16:30:00')
    now_time=time.fromisoformat(datetime.now().strftime('%H:%M:%S'))
    print(start_time<now_time<end_time)

# 按间距中的绿色按钮以运行脚本。
if __name__ == "__main__":
    normal_out()
