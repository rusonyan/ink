import sqlite3
import time
from loguru import logger

from PIL import ImageFont, Image, ImageDraw
from datetime import datetime,time
from config import CONFIG
from lib.util import write_new_pic

conn = sqlite3.connect('meets.db')

leval_four = ImageFont.truetype("static/fonts/siyuan.otf", 17)
min_font = ImageFont.truetype("static/fonts/siyuan.otf", 15)
title = ImageFont.truetype("static/fonts/ssm.otf", 15)
emoji_fonts = ImageFont.truetype("static/fonts/seguiemj.ttf", 15)


def room_convert(room_name: str):
    return room_name.replace("临", '').replace("楼", "F-").replace("+", "\n").replace("唐毅", '')


def name_list_convert(name_list: str):
    return name_list.replace('、', "  ")


def get_wrap_str(people, start_point=158):
    wrap_str = list(people)
    for x in range(0, len(wrap_str)):
        start_point = start_point + min_font.getlength(wrap_str[x])
        if start_point >= 400:
            wrap_str.insert(x, '\n')
            start_point = 158
    return ''.join(wrap_str)


def meet_print(left_top_point, room: str, name, time, people, d):
    d.line(((0, left_top_point), (400, left_top_point)), fill=0)
    room_name_control(left_top_point, room, is_long(people), d)
    d.text((65, left_top_point + 5), name, font=title, fill=0)
    d.text((65, left_top_point + 38), "🕔", font=emoji_fonts, fill=0)
    d.text((90, left_top_point + 31), time, font=min_font, fill=0)
    d.text((135, left_top_point + 36), "👥", font=emoji_fonts, fill=0)
    d.multiline_text((158, left_top_point + 31), get_wrap_str(people), font=min_font, fill=0)
    return is_long(people)


def is_long(people):
    return get_wrap_str(people).find("\n") != -1


def get_room_name_point(room_name, length=0):
    for x in list(room_name):
        length = length + min_font.getlength(x)
    return int((65 - length) / 2)


def multiline_get_room_name_point(room_name):
    room_name_list = room_name.split("\n")
    longest = room_name_list[0]
    for row in room_name_list:
        if len(row) > len(longest):
            longest = row
    return get_room_name_point(longest)


def room_name_control(left_top_point, room, flag, d):
    if flag:
        if room.find('\n') != -1:
            d.multiline_text((multiline_get_room_name_point(room), left_top_point + 16), room, font=min_font, fill=0)
        else:
            d.text((get_room_name_point(room), left_top_point + 25), room, font=min_font, fill=0)
    else:
        if room.find('\n') != -1:
            d.multiline_text((multiline_get_room_name_point(room), left_top_point + 6), room, font=min_font, fill=0)
        else:
            d.text((get_room_name_point(room), left_top_point + 20), room, font=min_font, fill=0)


def get_meeting(time: str):
    c = conn.cursor()
    return c.execute('''SELECT
                    MEET_NAME,
                    PEOPLE,
                    ROOM,
                    strftime('%H:%M',START_TIME ) AS s,
                    strftime('%H:%M',END_TIME ) AS e 
                FROM
                    COMPANY 
                WHERE
                    datetime( START_TIME ) <= datetime( ? ) 
                    AND 
                    datetime( ? ) <= datetime( END_TIME ) 
                ORDER BY
                    datetime( END_TIME ),
                    ROOM''', (time, time))


def img_init(d):
    emoji_font = ImageFont.truetype("static/fonts/seguiemj.ttf", 17)
    d.text((143, 3), get_meet_count() + "个会议进行中", font=leval_four, fill=0)
    d.text((115, 10), "💬", font=emoji_font, fill=0)


def meet_result_print():
    logger.info('当前会议:{}'.format(get_meeting(datetime.now().strftime("%Y-%m-%d %H:%M:%S")).fetchall()))


def handle(flag=0):
    meet_list = get_meeting(get_target_time()).fetchall()
    if len(meet_list) == 0:
        zero_out()
    else:
        while len(meet_list) > 0:
            meet_list = run(flag, meet_list)
            if len(meet_list) == 0:
                break
            import time
            time.sleep(CONFIG['sleep_time'])


def get_target_time():
    if time.fromisoformat(datetime.now().strftime('%H:%M:%S')) < time.fromisoformat('08:30:00'):
        return datetime.now().strftime("%Y-%m-%d 08:31:00")
    if time.fromisoformat('12:00:00') \
            < time.fromisoformat(datetime.now().strftime('%H:%M:%S')) \
            < time.fromisoformat('13:00:00'):
        return datetime.now().strftime("%Y-%m-%d 13:01:00")
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def zero_out():
    result = Image.new("1", (400, 300), 255)
    d = ImageDraw.Draw(result)
    img_init(d)
    result.save("out.jpg", "jpeg")
    result.close()


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


def output_control(d, flag, meet_list, left_top_point=30):
    logger.info('输出会议列表{}'.format(meet_list))
    for row in meet_list:
        if not is_long(row[1]) and left_top_point > 240:
            d.line(((0, left_top_point), (400, left_top_point)), fill=0)
            break
        if is_long(row[1]) and left_top_point > 225:
            d.line(((0, left_top_point), (400, left_top_point)), fill=0)
            break
        if meet_print(left_top_point, room_convert(row[2]), row[0], row[4], row[1], d):
            left_top_point = left_top_point + 75
        else:
            left_top_point = left_top_point + 60
        flag = flag + 1
    d.line(((0, left_top_point), (400, left_top_point)), fill=0)
    return flag


def get_meet_count():
    return str(len(get_meeting(time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")).fetchall()))


if __name__ == "__main__":
    handle()