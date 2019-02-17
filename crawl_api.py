import requests
import config
import tgalarm as tg


def get_now():
    import datetime
    now =str(datetime.datetime.now())[:10].replace('-','')
    return now

def get_weather_data():
    url = 'http://newsky2.kma.go.kr/service/SecndSrtpdFrcstInfoService2/ForecastSpaceData?' + \
    'serviceKey=' + key + \
    '&base_date=' + now_date + '&base_time=' + basetime + \
    '&nx=' + mokdong_nx + '&ny=' + mokdong_ny + \
    '&numOfRows=10' + '&pageNo=1' + '&_type=json'
    try:
        response = requests.get(url)
    except Exception as e:
        print('Crawling Error:', e)
    print(url)
    data = response.json()
    # return data['response']['body']['items']['item']
    data = data['response']['body']['items']['item']
    for item in data:
        print(item['category'])
    return data

def parse_data():
    data = get_weather_data()
    pty = sky = mn = mx = rain_per = False
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
    msg = '최저기온 : ' + str(mn) + '\n'  + '하늘 상태 : ' + sky + '\n' + '강우율 : ' + str(rain_per) + '% \n'  + '강우형태 :' + pty   
    return msg

    
if __name__ == '__main__':
    key = config.secret_key
    mokdong_nx = config.region['mokdong']['nx']
    mokdong_ny = config.region['mokdong']['ny']
    now_date = get_now() 
    basetime = '0200'
    msg = parse_data()
    tg.sendTo('weather', msg)
