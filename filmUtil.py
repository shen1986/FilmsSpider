from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import requests
import random
import time
import filmConfig as fc
import MongoOP as mop

# 获取页面
def get_page(link):
    # 反爬虫：每次请求都更改请求头
    ua = UserAgent()
    headers = {
        'User-Agent': ua.random
    }

    # 请求这个网站，并得到网站的内容
    r = requests.get(link, headers= headers)
    html = r.content # 使用r.content解封装
    html = html.decode('gbk') # 由gb2312解码为unicode
    soup = BeautifulSoup(html, 'lxml')
    return soup

# 解析网页
def get_data(filmName_list):
    scrap_times = 0  # 没爬一段时间加入一些长时间的休息
    for each in filmName_list:
        # 去除广告等其他内容
        if each['href'] == '/html/gndy/dyzz/index.html' or each['href'] == '/app.html':
            continue

        # 获取每个电影的详细内容
        filmName = each.text.strip()
        soup = get_page(fc.host + each['href'])
        content = soup.find('div', id="Zoom")
        pContent = content.find('p'); # 找到第一个P标签
        # with open('film.txt', 'a+', encoding='utf-8') as f:
        #     # 电影的详细内容解析
        #     for each in pContent:
        #         # 转成string类型，把多余的空格去掉
        #         eachone = str(each).strip()
        #         if len(eachone) == 0 or eachone == '<br>' or eachone == '<br/>':
        #             continue
        #
        #         # 把怕取出来的内容放到文件中去
        #         f.write(eachone + '\n')
        #     mySplit = fc.split * 100
        #     f.write(mySplit + '\n')
        #     f.close()
        newfilm = { 'name': filmName, 'content': '' }
        for each in pContent:
            # 转成string类型，把多余的空格去掉
            eachone = str(each).strip()
            if len(eachone) == 0 or eachone == '<br>' or eachone == '<br/>':
                continue

            newfilm['content'] += eachone + '\n'

        mop.filmCollection.insert_one(newfilm)

        # 以免被反爬虫，每爬一个网页就休息会, 且间隔时间不一样。
        # 每爬5条，就休息10s钟。
        scrap_times += 1
        if scrap_times % 5 == 0:
            sleep_time = 10 + random.random()
        else:
            sleep_time = random.randint(0,2) + random.random()
        time.sleep(sleep_time)