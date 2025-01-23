# Lottery_Yueshan_Spring_Festival_Gala
Lottery code for the Spring Festival Gala in Yueshan Village
月山村春晚专用抽奖代码


# 开发环境
conda create -n yueshan python=3.10

conda activate yueshan

pip install ttkbootstrap tk pyinstaller

pip install Pillow==11.1.0

# 打包
pyinstaller --onefile --windowed main.py

# to do
+ 抽奖的时候滚动显示名字最终停止在某人名字上
