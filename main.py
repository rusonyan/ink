import datetime
import os

import requests
from PIL import ImageFont, Image, ImageDraw
from bs4 import BeautifulSoup

fonts_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'fonts')

max_font = ImageFont.truetype('fonts/siyuan.otf', 35)
leval_two = ImageFont.truetype('fonts/timing.otf', 30)
leval_three = ImageFont.truetype('fonts/siyuan.otf', 20)
leval_four = ImageFont.truetype('fonts/siyuan.otf', 17)
min_font = ImageFont.truetype('fonts/siyuan.otf', 15)
normal_font=ImageFont.truetype('fonts/siyuan.otf', 5)
emoji_font=ImageFont.truetype('fonts/seguiemj.ttf', 17)

result = Image.new("1", (400, 300), 255)
d = ImageDraw.Draw(result)
d.rectangle(((0, 0), (400, 30)), fill=0)
d.text((140, 3), '正在进行的会议', font=leval_four, fill=255)
d.text((115, 10), '💬', font=emoji_font, fill=255)


def normal_out():
    d.rectangle(((0, 60), (400, 90)), fill=0)
    d.rectangle(((0, 120), (400, 150)), fill=0)
    d.rectangle(((0, 180), (400, 210)), fill=0)
    d.rectangle(((0, 240), (400, 270)), fill=0)


    result.save("out.jpg", "jpeg")

# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    normal_out()


