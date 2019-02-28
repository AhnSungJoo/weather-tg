# -*- coding: utf-8 -*-
from urllib import request 
import json
import requests
import config
import tgalarm as tg
import xmltodict, json
import crawl_naver as cn

def get_now():
    import datetime
    now = str(datetime.datetime.now())[:10]
    # date_time = datetime.datetime.strptime(now, "%Y-%m-%d %H:%M:%S")
    # date_time -= datetime.timedelta(days=1)
    # date_time = str(date_time)[:10]
    return now.replace('-', '')

def get_weather_data(key, nx, ny):
    datas = []
    for basetime in config.basetimes:
        url = 'http://newsky2.kma.go.kr/service/SecndSrtpdFrcstInfoService2/ForecastSpaceData?' + \
        'serviceKey=' + key + \
        '&base_date=' + now_date + '&base_time=' + basetime + \
        '&nx=' + nx + '&ny=' + ny + \
        '&numOfRows=10' + '&pageNo=1' + '&_type=json'
        try:
            response = requests.get(url)
        except Exception as e:
            print('Crawling Weather data Error:', e)
        data = response.json()
        # print(data)
        if data != [] or data != None:
            data = data['response']['body']['items']['item']
            datas.append(data)
    return datas

def get_dust_data(key):
    url = 'http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getCtprvnMesureLIst?' + \
    'serviceKey=' + key + \
    '&numOfRows=10&pageNo=1&itemCode=PM10&dataGubun=HOUR&searchCondition=MONTH'
    try:
        response = request.urlopen(url).read().decode('utf-8')
        # res = requests.get(url)
    except Exception as e:
        print('Crawling dust data Error:', e)

    o = xmltodict.parse(response)
    return json.dumps(o)

 


def parse_weather_data():
    key = config.secret_key
    weather_msg = '- 오늘의 날씨 - \n'
    for region in config.regions.keys():
        nx = config.regions[region]['nx']
        ny = config.regions[region]['ny']
        datas = get_weather_data(key, nx, ny)
        # print(datas)
        pty = sky = mn = mx = rain_per = False
        msg = ''
        if region == 'mokdong':
            msg = '목동 날씨 \n'
        elif region == 'uiwang':
            msg = '의왕 날씨 \n'
        elif region == 'pyeongchon':
            msg = '평촌 날씨 \n'
        elif region == 'gunpo':
            msg = '군포 날씨 \n'
        elif region == 'sankok':
            msg = '산곡 날씨 \n'
        elif region == 'pankyo':
            msg = '판교 날씨 \n'
        elif region == 'gangnam':
            msg = '강남 날씨 \n'
        elif region == 'sinchon':
            msg = '신촌 날씨\n'
        elif region == 'wonju':
            msg = '원주 날씨\n'

        for data in datas:
            for item in data:
                if item['category'] == 'TMN':
                    mn = item['fcstValue']
                elif item['category'] == 'TMX':
                    mx = item['fcstValue']
                elif item['category'] == 'POP':
                    rain_per = item['fcstValue']
                elif item['category'] == 'SKY':
                    sky = item['fcstValue']
                elif item['category'] == 'PTY':
                    pty = item['fcstValue']
            
            if sky is not False:
                if sky == 1:
                    sky = '맑음'
                elif sky == 2:
                    sky = '구름 조금'
                elif sky == 3:
                    sky = '구름 많음'
                elif sky == 4:
                    sky = '흐림'        
            if pty is not False:
                if pty == 0:
                    pty = '없음'
                elif pty == 1:
                    pty = '비'
                elif pty == 2:
                    pty = '비/눈'
                elif pty == 3:
                    pty = '눈'

        mn, mx = cn.parse_temper_weather(msg)
        dust = cn.parse_dust(msg)
        msg += '최저기온 : ' + str(mn) + '\n' + '최고기온 :' + str(mx) + '\n'  + '하늘 상태 : ' + sky + '\n' + '강우율 : ' + str(rain_per) + '% \n'  + '강우형태 :' + pty + '\n미세먼지: ' + dust + '\n'   
        weather_msg += msg
    return weather_msg
        

if __name__ == '__main__':
    now_date = get_now() 
    msg = parse_weather_data()
    print(msg)
    tg.sendTo('weather', msg)

