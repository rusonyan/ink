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
emoji_font = ImageFont.truetype('fonts/seguiemj.ttf', 20)
emoji_two_font = ImageFont.truetype('fonts/seguiemj.ttf', 15)

skycon = {"CLEAR_DAY": "晴日",
          "CLEAR_NIGHT": "晴夜",
          "PARTLY_CLOUDY_DAY": "多云日",
          "PARTLY_CLOUDY_NIGHT": "多云夜",
          "CLOUDY": "阴天",
          "LIGHT_HAZE": "轻度雾霾",
          "MODERATE_HAZE": "中度雾霾",
          "HEAVY_HAZE": "重度雾霾",
          "LIGHT_RAIN": "小雨",
          "MODERATE_RAIN": "中雨",
          "HEAVY_RAIN": "大雨",
          "STORM_RAIN": "暴雨",
          "FOG": "雾",
          "LIGHT_SNOW": "小雪",
          "MODERATE_SNOW": "中雪",
          "HEAVY_SNOW": "大雪",
          "DUST": "浮尘",
          "SAND": "沙尘",
          "WIND": "风"}

result = Image.new("1", (400, 300), 255)
d = ImageDraw.Draw(result)
d.line(((0, 270), (400, 270)))
d.line(((133, 270), (133, 300)))
d.line(((266, 270), (266, 300)))


def insert(strs):
    if len(strs) < 24:
        return strs
    str_list = list(strs)
    str_list.insert(22, '\n')
    return ''.join(str_list)


def get_describe():
    return BeautifulSoup(requests.get('https://www.qweather.com/weather/huangpu-101020400.html').content,
                         "html.parser").find('div', class_='current-abstract').getText().strip()


def normal_out(w_state, temperature, skycon, describe: str, comfort, humidity, air_quality):
    icon = Image.open("img/" + w_state + ".png").resize((90, 90), Image.LANCZOS)
    result.paste(icon, (120, 70), icon)
    d.text((0, 0), '金砖大厦', font=leval_three, fill=0)
    d.text((310, 8), datetime.date.today().strftime('%Y-%m-%d'), font=min_font, fill=0)
    d.rounded_rectangle((325, 30, 383, 50), 5, width=1)
    d.text((332, 28), '空气' + air_quality, font=min_font, fill=0)
    d.text((220, 70), str(int(temperature)) + '°', font=max_font, fill=0)
    d.text((220, 120), skycon, font=leval_three, fill=0)
    d.multiline_text((35, 185), insert(describe), font=leval_four, fill=0)
    d.text((40, 283), '🌡', font=emoji_two_font, fill=0)
    d.text((55, 275), comfort, font=leval_four, fill=0)
    d.text((170, 275), "2个会议", font=leval_four, fill=0)
    d.text((310, 283), '💧', font=emoji_two_font, fill=0)
    d.text((325, 275), str(int(humidity)) + '%', font=leval_four, fill=0)
    result.save("out.jpg", "jpeg")


def handle():
    caiyun = requests.get('https://api.caiyunapp.com/v2.6/rpH8cgFaDop4WkXX/121.5035,31.2331/realtime').json()[
        'result']['realtime']
    normal_out(caiyun["skycon"],
               caiyun["temperature"],
               skycon[caiyun["skycon"]],
               get_describe(),
               caiyun["life_index"]["comfort"]["desc"],
               caiyun["humidity"] * 100,
               caiyun['air_quality']["description"]["chn"])


if __name__ == '__main__':
    handle()
