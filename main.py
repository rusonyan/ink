from datetime import datetime
from PIL import ImageFont, Image, ImageDraw

from lib.util import write_new_pic


def normal_out(left_top_point=30):
    # result = Image.new("1", (400, 300), 255)
    # target = Image.open('static/photo/out.jpg')
    # target.resize((400,300))
    # result.paste(target, (0, 0))
    # result.save("out.jpg", "jpeg")
    PNG = Image.open('out.jpg').convert('LA')
    gray = PNG.convert('L')
    bw = gray.point(lambda x: 0 if x<200 else 255, '1')#Turn into bitmap and color flip
    bw =bw.resize((400,300),Image.ANTIALIAS)
    bw.save('out.jpg')#save Picture

# 按间距中的绿色按钮以运行脚本。
if __name__ == "__main__":
    #normal_out()
    write_new_pic()
