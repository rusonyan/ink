from datetime import datetime


def normal_out(left_top_point=30):
    now = datetime.now()
    start = datetime(year=now.year, month=now.month, day=now.day, hour=0)
    end = datetime(year=now.year, month=now.month, day=now.day, hour=23)
    print(start)


# 按间距中的绿色按钮以运行脚本。
if __name__ == "__main__":
    normal_out()
