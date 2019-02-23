from urllib.request import urlopen, Request
import urllib
import bs4


def parse_max_weather(location):
    # location = '목동 날씨'
    parse_location = urllib.parse.quote(location)
    url = 'https://search.naver.com/search.naver?ie=utf8&query='+ parse_location
    req = Request(url)
    page = urlopen(req)
    html = page.read()
    soup = bs4.BeautifulSoup(html, features='lxml')
    return soup.find('span',class_='max').text

# print(type(parse_max_weather('목동 날씨')))
# regions = ['목동 날씨', '의왕 날씨', '평촌 날씨', '강남 날씨', '군포 날씨','산곡 날씨', '판교 날씨', '강남 날씨']
# for region in regions:
#     print(parse_max_weather(region))
