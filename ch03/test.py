# coding=utf-8
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.Qt import Qt

# coding=utf-8
import requests
from bs4 import BeautifulSoup
def g_c(city):
    url = "http://toy1.weather.com.cn/search"
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
    }
    params = {
        'cityname':city
    }
    response = requests.get(url, headers=header,params=params)
    citys = response.content.decode("utf-8")
    if city in citys:
        start = citys.find(':')
        end = citys.find("~")
        cityid = citys[start+2:end]
    else:
        cityid = False
    return cityid


def g_1dw(city):
    cityid = g_c(city)
    if cityid:
        url = 'http://www.weather.com.cn/weather1d/' + str(cityid) + '.shtml'
        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
        }
        response = requests.get(url, headers=header)
        html = response.content.decode("utf-8")
        soup = BeautifulSoup(html, 'lxml')

        weather_info = {
            "title": None,
            "wea": None,
            "tem": None,
            "win": None,
            "sun": None
        }

    # 今日天气
        weather = {
            "daytime": weather_info,
            "night": weather_info.copy()
        }

    # 定义到class属性值为"t"的div标签
        div_tag = soup.find_all("div", attrs={"class": "t"})[0]
    # 抓取白天的天气
    # 标题
        weather['daytime']['title'] = div_tag.find_all("h1")[0].get_text()
    # 天气
        weather['daytime']['wea'] = soup.find_all("p", attrs={"class": "wea"})[0].get_text()
    # 温度
        weather['daytime']['tem'] = div_tag.find_all("p", attrs={"class": "tem"})[0].get_text().replace("\n", "")
    # 风速
        weather['daytime']['win'] = div_tag.find_all("p", attrs={"class": "win"})[0].get_text().replace("\n", "")
    # 日落时间
        weather['daytime']['sun'] = div_tag.find_all("p", attrs={"class": "sun"})[0].get_text().replace("\n", "")

    # 抓取夜间天气
    # 标题
        weather['night']['title'] = div_tag.find_all("h1")[1].get_text()
    # 天气
        weather['night']['wea'] = div_tag.find_all("p", attrs={"class": "wea"})[1].get_text()
    # 温度
        weather['night']['tem'] = div_tag.find_all("p", attrs={"class": "tem"})[1].get_text().replace("\n", "")
    # 风速
        weather['night']['win'] = div_tag.find_all("p", attrs={"class": "win"})[1].get_text().replace("\n", "")
    # 日落时间
        weather['night']['sun'] = div_tag.find_all("p", attrs={"class": "sun"})[1].get_text().replace("\n", "")
        return weather
    else:
        return False


def spider_7dweather(city):
    cityid = g_c(city)
    if cityid:
        url = 'http://www.weather.com.cn/weather/' + str(cityid) + '.shtml'

        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36"
                          " (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36"
        }

        response = requests.get(url, headers=header)
        html = response.content.decode("utf-8")
        soup = BeautifulSoup(html, 'lxml')

        weather_info = {
            "title": None,
            "wea": None,
            "tem": None,
            "win": None,
        }
    # 7日天气
        weather = dict()
        for i in range(7):
            weather[str(i)] = weather_info.copy()

        ul_tag = soup.find_all("ul", attrs={"class": "t clearfix"})[0]
        for i in range(7):
            li_tag = ul_tag.find_all("li")[i]
        # 标题
            weather[str(i)]['title'] = li_tag.h1.get_text()
        # 天气
            weather[str(i)]['wea'] = li_tag.find_all("p")[0].get_text()
        # 风速
            weather[str(i)]['win'] = li_tag.find_all("p")[1].get_text().replace("\n", "")
        # 温度上限
            weather[str(i)]['tem'] = li_tag.find_all("p")[2].get_text().replace("\n", "")
        return weather
    else:
        return False

print(g_1dw("武汉"))

# class Myweather():
#     def __init__(self):
#         self.app = QApplication(sys.argv)
#         # 创建一个窗体
#         self.window = QWidget()
#         # 设置窗体位置大小
#         self.window.setGeometry(300, 300, 400, 600)
#         # 设置窗体标题
#         self.window.setWindowTitle("编玩边学制作")
#         # 设置标题图标
#         self.window.setWindowIcon(QIcon("img/bwbx.png"))
#         # 创建网格布局管理器
#         grid = QGridLayout()
#         # 设置网格间隔
#         grid.setSpacing(10)
#         # 网格布局
#         self.window.setLayout(grid)
#
#         # 创建标题
#         self.lb_search = QLabel('天气查询')
#         self.lb_search.setAlignment(Qt.AlignCenter)
#         self.lb_search.setFont(QFont("Times",21))
#         grid.addWidget(self.lb_search, 0, 0, 1, 2)
#         # 本地信息
#         self.lb_city = QLabel("城市：")
#         self.lb_city.setAlignment(Qt.AlignCenter)
#         self.lb_city.setFont(QFont('Times', 16))
#         grid.addWidget(self.lb_city, 1, 0, 1, 1)
#         # 城市输入框
#         self.edit_city = QLineEdit()
#         self.edit_city.setFont(QFont('Times', 16))
#         grid.addWidget(self.edit_city, 1, 1, 1, 1)
#         # 今日天气
#         self.btn_1d = QPushButton('查看今天天气')
#         self.btn_1d.setFont(QFont('Times', 13))
#         grid.addWidget(self.btn_1d,2,0,1,1)
#         # 7日天气
#         self.btn_7d =QPushButton('查看未来7天天气')
#         self.btn_7d.setFont(QFont('Times', 13))
#         grid.addWidget(self.btn_7d, 2, 1, 1, 1)
#         # 展示区
#         self.weather_info = QTextBrowser()
#         self.weather_info.setText('这里用来展示天气信息')
#         self.weather_info.setFont(QFont('Times', 13))
#         grid.addWidget(self.weather_info, 3, 0, 1, 2)
#     # 展示今日的天气
#     def set_1d_weather(self):
#         text = self.edit_city.text()
#         data = ''
#         if text:
#             ret = g_1dw(text)
#             if ret:
#                 for key,val in ret['daytime'].items():
#                     if val:
#                         data += val + '\n'
#             # 夜间
#                 data += '\n'
#                 for key,val in ret['night'].items():
#                     if val:
#                         data += val + '\n'
#         self.weather_info.setText(data)
#     # 展示未来7天天气
#     def set_7d_weather(self):
#         text = self.edit_city.text()
#         data = ''
#         if text:
#             ret = spider_7dweather(text)
#             if ret:
#                 for i in range(7):
#                     for key, val in ret[str(i)].items():
#                         if val:
#                             data += val + '\n'
#                     data += '\n'
#         self.weather_info.setText(data)
#     def run(self):
#         # 事件绑定
#         self.btn_1d.clicked.connect(self.set_1d_weather)
#         self.btn_7d.clicked.connect(self.set_7d_weather)
#         # 显示窗体
#         self.window.show()
#         # 退出时清理
#         self.app.exec_()
#
# app = Myweather()
# app.run()