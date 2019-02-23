# -*- coding: utf-8 -*-
from urllib.request import urlopen, Request
import urllib
import bs4


def parse_max_weather(location):
    # location = '목동 날씨'
    location = location.replace('\n', '')
    parse_location = urllib.parse.quote(location)
    url = 'https://search.naver.com/search.naver?ie=utf8&query='+ parse_location
    req = Request(url)
    page = urlopen(req)
    html = page.read()
    soup = bs4.BeautifulSoup(html, features='lxml')
    return soup.find('span',class_='max').text