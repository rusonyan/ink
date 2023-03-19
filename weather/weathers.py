import datetime
import os

import requests
from PIL import ImageFont, Image, ImageDraw
from bs4 import BeautifulSoup
from loguru import logger
from meet.meets import get_meet_count

fonts_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), '../static/fonts')

max_font = ImageFont.truetype('static/fonts/siyuan.otf', 35)
leval_two = ImageFont.truetype('static/fonts/timing.otf', 30)
leval_three = ImageFont.truetype('static/fonts/siyuan.otf', 20)
leval_four = ImageFont.truetype('static/fonts/siyuan.otf', 17)
min_font = ImageFont.truetype('static/fonts/siyuan.otf', 15)
emoji_font = ImageFont.truetype('static/fonts/seguiemj.ttf', 20)
emoji_two_font = ImageFont.truetype('static/fonts/seguiemj.ttf', 15)

skycon = {"CLEAR_DAY": "晴日",
          "CLEAR_NIGHT": "晴夜",
          "PARTLY_CLOUDY_DAY": "多云",
          "PARTLY_CLOUDY_NIGHT": "多云",
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


def insert(strs):
    if len(strs) < 24:
        return strs
    str_list = list(strs)
    str_list.insert(20, '\n')
    return ''.join(str_list)


def get_describe():
    return BeautifulSoup(requests.get('https://www.qweather.com/weather/huangpu-101020400.html').content,
                         "html.parser").find('div', class_='current-abstract').getText().strip()


def normal_out(w_state, temperature, skycon, comfort, humidity, air_quality, result, d):
    icon = Image.open("static/img/" + w_state + ".png").resize((90, 90), Image.LANCZOS)
    result.paste(icon, (120, 100), icon)
    result.paste(icon, (120, 100), icon)
    d.text((0, 0), '新辰·临港', font=leval_three, fill=0)
    d.text((310, 8), datetime.date.today().strftime('%Y-%m-%d'), font=min_font, fill=0)
    d.rounded_rectangle((325, 30, 383, 50), 5, width=1)
    d.text((332, 28), '空气' + air_quality, font=min_font, fill=0)
    d.text((220, 100), str(int(temperature)) + '°', font=max_font, fill=0)
    d.text((220, 145), skycon, font=leval_three, fill=0)
    # d.multiline_text((35, 200), insert('临港的' + describe), font=leval_four, fill=0)
    d.text((40, 283), '🌡', font=emoji_two_font, fill=0)
    d.text((55, 275), comfort, font=leval_four, fill=0)
    d.text((170, 275), get_meet_count() + "个会议", font=leval_four, fill=0)
    d.text((310, 283), '💧', font=emoji_two_font, fill=0)
    d.text((325, 275), str(int(humidity)) + '%', font=leval_four, fill=0)
    result.save("out.jpg", "jpeg")
    result.close()


def init(d):
    d.line(((0, 270), (400, 270)))
    d.line(((133, 270), (133, 300)))
    d.line(((266, 270), (266, 300)))


def handle():
    result = Image.new("1", (400, 300), 255)
    d = ImageDraw.Draw(result)
    init(d)
    caiyun = requests.get('https://api.caiyunapp.com/v2.6/rpH8cgFaDop4WkXX/121.9315,30.9089/realtime').json()[
        'result']['realtime']
    # weather_description = get_describe()
    logger.info("天气数据源:{}".format(caiyun))
    normal_out(caiyun["skycon"],
               caiyun["temperature"],
               skycon[caiyun["skycon"]],
               # weather_description,
               caiyun["life_index"]["comfort"]["desc"],
               caiyun["humidity"] * 100,
               caiyun['air_quality']["description"]["chn"],
               result, d)


if __name__ == '__main__':
    handle()
