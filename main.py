import datetime
import os

import requests
from PIL import ImageFont, Image, ImageDraw
from bs4 import BeautifulSoup

fonts_dir = os.path.join(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "static/fonts"
)

max_font = ImageFont.truetype("fonts/siyuan.otf", 35)
leval_two = ImageFont.truetype("fonts/timing.otf", 30)
leval_three = ImageFont.truetype("fonts/siyuan.otf", 20)
leval_four = ImageFont.truetype("fonts/siyuan.otf", 17)
min_font = ImageFont.truetype("fonts/siyuan.otf", 15)

title = ImageFont.truetype("fonts/ssm.otf", 15)
# title = ImageFont.truetype("fonts/ssm3.otf", 15)

normal_font = ImageFont.truetype("fonts/siyuan.otf", 5)
emoji_font = ImageFont.truetype("fonts/seguiemj.ttf", 17)
emoji_fonts = ImageFont.truetype("fonts/seguiemj.ttf", 15)

result = Image.new("1", (400, 300), 255)
d = ImageDraw.Draw(result)
# d.rectangle(((0, 0), (400, 30)), fill=0)

d.text((140, 3), " 正在进行的会议", font=leval_four, fill=0)
# d.text((140, 70), '还剩', font=min_font, fill=0)
# d.text((140, 100), '11天', font=title, fill=0)
d.text((115, 10), "💬", font=emoji_font, fill=0)

flage = False


def get_wrap_str(people, start_point=158):
    wrap_str = list(people)
    for x in range(0, len(wrap_str)):
        start_point = start_point + min_font.getlength(wrap_str[x])
        if start_point >= 400:
            wrap_str.insert(x, '\n')
            start_point = 158
    return ''.join(wrap_str)


def meet_print(left_top_point, room, name, time, people):
    d.line(((0, left_top_point), (400, left_top_point)), fill=0)
    d.text((10, left_top_point + 25), room, font=min_font, fill=0)
    d.text((65, left_top_point + 5), name, font=title, fill=0)
    d.text((65, left_top_point + 38), "🕔", font=emoji_fonts, fill=0)
    d.text((90, left_top_point + 31), time, font=min_font, fill=0)
    d.text((135, left_top_point + 36), "👥", font=emoji_fonts, fill=0)
    d.multiline_text((158, left_top_point + 31), get_wrap_str(people), font=min_font, fill=0)


def normal_out(left_top_point=30):
    # while(left_top_point<=300):
    #    #
    #
    #
    meet_print(30, "9F-4会", "青年理论小组第十六小组讨论会", "12:00", "青年理论小组第十六小组成员")
    meet_print(90, "金4会", "UI双周工作汇报会", "14:00", "于洁  林层林  张梅  杨垒佳")
    meet_print(150, "金2会", "故宫书店项目运营工作讨论", "14:30", "冯总 杨波  申卓雨  李总  阅外滩书店杨总")
    meet_print(225, "9F-2会", "杭州地铁每日夕会", "16:30", "汪靖 涛涛  朱江成  叶健豪  左毅")
    #
    result.save("out.jpg", "jpeg")


# 按间距中的绿色按钮以运行脚本。
if __name__ == "__main__":
    normal_out()
