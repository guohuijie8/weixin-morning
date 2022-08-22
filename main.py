from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]

#获取今日天气weather，high温度，low温度
def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]    #[0]返回的是今日天气  明天[1]
  return weather['weather'], math.floor(weather['high']), math.floor(weather['low'])     #return weather['weather'], math.floor(weather['temp'])

#计算在一起时间
def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d") + 1  #delta=今天datetime.now()-开始时间  strptime把时间字符串解析为时间元组
  return delta.days

#计算生日
def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")   #next(下一次生日：年-月-日)
  if next < datetime.now():                                                       #如果下一次生日时间小于今天，next(下一次生日）=下一年的生日
    next = next.replace(year=next.year + 1)
  return (next - today).days + 1  #返回日期+1

#获取语句
def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:   #status_code表示服务器的响应状态，如200代表服务器正常响应
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature = get_weather()
data = {"weather":{"value":wea},"temperature":{"value":temperature},"love_days":{"value":get_count()},"birthday_left":{"value":get_birthday()},"words":{"value":get_words(), "color":get_random_color()}}
res = wm.send_template(user_id, template_id, data)
print(res)
