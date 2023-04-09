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

