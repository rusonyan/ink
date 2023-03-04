import sqlite3
import time
from datetime import datetime
from loguru import logger

from PIL import ImageFont, Image, ImageDraw

from lib.util import write_new_pic
from meet.meets import leval_four, output_control

conn = sqlite3.connect('meets.db')


def get_meeting():
    now = datetime.now()
    c = conn.cursor()
    return c.execute('''SELECT
                            MEET_NAME,
                            PEOPLE,
                            ROOM,
                            strftime( '%H:%M', START_TIME ) AS s,
                            strftime( '%H:%M', END_TIME ) AS e 
                        FROM
                            "COMPANY" 
                        WHERE
                            PEOPLE LIKE '%闫瑞松%' 
                                AND 
                            datetime( START_TIME ) >= datetime(?) 
                                AND 
                            datetime( END_TIME ) <= datetime(?)
                        ORDER BY
                            START_TIME
                            ''', (datetime(year=now.year, month=now.month, day=now.day, hour=0),
                                  datetime(year=now.year, month=now.month, day=now.day, hour=23)))


def img_init(d):
    emoji_font = ImageFont.truetype("static/fonts/seguiemj.ttf", 17)
    d.text((143, 3), '今日您有' + get_meet_count() + "个会议", font=leval_four, fill=0)
    d.text((115, 10), "👁", font=emoji_font, fill=0)


def meet_result_print():
    logger.info(get_meeting())


def handle(flag=0):
    meet_list = get_meeting().fetchall()
    logger.info(meet_list)
    if len(meet_list) == 0:
        zero_out()
    else:
        while len(meet_list) > 0:
            meet_list = run(flag, meet_list)
            if len(meet_list) == 0:
                break
            time.sleep(600)


def run(flag, meet_list):
    result = Image.new("1", (400, 300), 255)
    d = ImageDraw.Draw(result)
    img_init(d)
    meet_result_print()
    flag = output_control(d, flag, meet_list)
    result.save("out.jpg", "jpeg")
    result.close()
    write_new_pic()
    meet_list = meet_list[flag:]
    return meet_list


def zero_out():
    result = Image.new("1", (400, 300), 255)
    d = ImageDraw.Draw(result)
    img_init(d)
    result.save("out.jpg", "jpeg")
    result.close()


def get_meet_count():
    return str(len(get_meeting().fetchall()))


if __name__ == "__main__":
    handle()
