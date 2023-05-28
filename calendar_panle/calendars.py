import os
import time
from datetime import datetime
from PIL import ImageFont, Image, ImageDraw

fonts_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), '../static/fonts')

max_font = ImageFont.truetype('static/fonts/siyuan.otf', 35)
day_font = ImageFont.truetype('static/fonts/SourceHanSerifCN-Regular-1.otf', 95)
month_font = ImageFont.truetype('static/fonts/SourceHanSerifCN-Regular-1.otf', 20)
time_font = ImageFont.truetype('static/fonts/Arimo-Regular.ttf', 20)

month_list = ['一月', '二月', '三月',
              '四月', '五月', '六月',
              '七月', '八月', '九月',
              '十月', '十一月', '十二月']
week_list = [
    '周一',
    '周二',
    '周三',
    '周四',
    '周五',
    '周六',
    '周日'
]


def init(d):
    d.line(((0, 270), (400, 270)))
    d.line(((133, 270), (133, 300)))
    d.line(((266, 270), (266, 300)))


def handle():
    result = Image.new("1", (400, 300), 255)
    d = ImageDraw.Draw(result)
    day = time.strftime("%d", time.localtime())
    month = month_list[int(time.strftime('%m', time.localtime())) - 1]
    now_time = time.strftime("%H:%M", time.localtime())
    week = week_list[datetime.now().weekday()]
    d.text((30, 15), day, font=day_font, fill=0)
    d.text((30, 150), month, font=month_font, fill=0)
    d.text((30, 200), '二 零 二 三 年', font=month_font, fill=0)
    d.text((300, 170), now_time, font=time_font, fill=0)
    d.text((305, 220), week, font=month_font, fill=0)

    d.line(((30, 190), (200, 190)), fill=0, width=2)
    d.line(((30, 240), (200, 240)), fill=0, width=2)

    d.rectangle((280, 150, 370, 270), fill=None, width=2)

    result.save("out.jpg", "jpeg")
    result.close()


if __name__ == '__main__':
    handle()
