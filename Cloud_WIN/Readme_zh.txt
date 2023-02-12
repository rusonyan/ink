Cloud ESP32 e-Paper Board Host程序简明使用说明

注意：
1.因为windows环境比较复杂，而且一个系统下可能存在多个版本，请自行用可以正常使用的python3替代下文的python。
2.因为正常情况下windows安装python时会自动安装pip，这里不对pip安装进行讲解。
3.因为windows防火墙的缘故，需要关闭或者允许python通过windows防火墙

1.安装必要库
python -m pip install tqdm
python -m pip install numpy
python -m pip install pillow
python -m pip install pypiwin32
python -m pip install progressbar


2.程序
在当前目录下运行（CMD、PowerShell）

python ./examples/***inch_display_EPD

该程序会根据程序生成对应尺寸的图形和读取一张图片并发送给从机显示

示例：

如果使用4.2inch e-Paper Cloud Module
python ./examples/4.2inch_display_EPD

如果使用2.13inch e-Paper Cloud Module
python ./examples/2.13inch_display_EPD

注：以上程序连接和结束均会被记录在Histroy.txt中

