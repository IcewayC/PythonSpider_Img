# -*- coding: utf-8 -*-
import requests
import threading
from lxml import etree #解析网页
from bs4 import BeautifulSoup


def get_html(html):#获取页面html代码
    # url = 'https://www.doutula.com/article/list/?page=1'
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0'}
    request = requests.get(url=html, headers=headers)
    response = request.content
    # print response
    return response


def get_img_html(html):#获取图片
    soup = BeautifulSoup(html, 'lxml')
    all_a = soup.find_all('a', class_='list-group-item')
    for i in all_a:
        print i['href']
        img_html = get_html(i['href'])#获取图片html地址
        get_img(img_html)#获取图片


def get_img(html):#获取图片
    soup = etree.HTML(html)#自动修正html源码
    items = soup.xpath('//div[@class="artile_des"]')#解析网页方法
    for item in items:
        imgurl_list = item.xpath('table/tbody/tr/td/a/img/@onerror')#图片url地址
        start_save_img(imgurl_list)#启动线程


def save_img(img_url):
    img_url = img_url.split('=')[-1][1:-2].replace('jp', 'jpg')
    print '正在下载：http:' + img_url
    img_content = requests.get('http:' + img_url).content
    with open('img/%s' % img_url.split('/')[-1], 'wb') as f:
        f.write(img_content)


def start_save_img(imgurl_list):
    for i in imgurl_list:
        th = threading.Thread(target=save_img, args=(i,))
        th.start()


def main():
    start_url = 'https://www.doutula.com/article/list/?page='
    for i in range(1, 5):
        start_html = get_html(start_url.format(i))
        get_img_html(start_html)


if __name__ == '__main__':
    main()
