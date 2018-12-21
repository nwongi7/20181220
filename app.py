from flask import Flask, render_template, request
from bs4 import BeautifulSoup as bs
import time
import requests
import json
import random

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/lotto')
def lotto():

    numbers = list(range(1,46))
    
    lotto = random.sample(numbers,6)
    lotto = sorted(lotto, key=int)
    print(lotto)
    
    numbs=[]
    text = ["첫 번째","두 번째","세 번째","네 번째","다섯 번째","여섯 번째"]
    for i in list(range(6)):
        letter=("이번 주 {} 로또 추천 번호는 {} 입니다.".format(text[i],lotto[i]))
        numbs.append(letter)
    print(numbs)
    return render_template('lotto.html')
    
    
@app.route('/toon')
def toon():
    cat = request.args.get('type')
    today = time.strftime("%a").lower()
    
    if(cat == 'naver'):
        #네이버 웹툰
        naver_url = 'https://comic.naver.com/webtoon/weekdayList.nhn?week='+today
        url_base = 'https://comic.naver.com'
        response = requests.get(naver_url).text
        soup = bs(response,'html.parser')
        
        toons = []
        li = soup.select('.img_list li')
        for item in li:
            toon = {
                "title" : item.select_one('dt a')['title'],
                "url" : url_base + item.select('dt a')[0]['href'],
                "img_url" : item.select('.thumb img')[0]['src']
            }
            toons.append(toon)
        return render_template('toon.html', t = toons, cat = cat)
        
    elif(cat == 'daum'):
        #다음 웹툰
        daum_url = 'http://webtoon.daum.net/data/pc/webtoon/list_serialized/'+today
        url_base = 'http://webtoon.daum.net/webtoon/view/'
        response = requests.get(daum_url).text
        document = json.loads(response)
        
        toons = []
        data = document['data']
        for toon in data:
            toon = {
              "title" : toon['title'],
              "url" : url_base + toon['nickname'],
              "img_url" : toon['pcThumbnailImage']['url']
            }
            toons.append(toon)
        return render_template('toon.html', t = toons, cat = cat)


@app.route('/apart')
def apart():
    #1. 내가 원하는 정보를 얻을 수 있는 url을 url 변수에 저장한다.
    url = "http://rt.molit.go.kr/new/gis/getDanjiInfoDetail.do?menuGubun=A&p_apt_code=20355962&p_house_cd=1&p_acc_year=2018&areaCode=&priceCode="
    #1-1. requests header에 추가할 정보를 dictionary 형태로 저장한다.
    headers = {
        "Host": "rt.molit.go.kr",
        "Referer": "http://rt.molit.go.kr/new/gis/srh.do?menuGubun=A&gubunCode=LAND"
    }
    #2. requests 의 get 기능을 이용하여 해당 url에 header와 함께 요청을 보낸다
    response = requests.get(url, headers = headers).text
    #3. 응답으로 온 코드의 형태를 살펴본다.(json/xml/html)
    #위치(JIBUN_NAME), 아파트 이름(BLDG_NM), 실거래가(SUM_AMT), 실거래월(DEAL_MM, DEAL_DD), 전용면적(BLDG_AREA)
    document = json.loads(response)
    print(document)
    
    for d in document["result"]:
        print(d["BLDG_NM"])
        
    return render_template('/apart.html')
    
    
@app.route('/exchange')
def exchange():
    url = 'https://www.x-rates.com/table/?from=USD&amount=1'
    response = requests.get(url).text
    soup = bs(response,'html.parser')
    
    ##content > div:nth-child(1) > div > div.col2.pull-right.module.bottomMargin > div.moduleContent > table.tablesorter.ratesTable > tbody > tr:nth-child(1) > td:nth-child(2)
    
    soup.select('.moduleContent .tablesorter tbody tr')[0]
    excs = []
    li = soup.select('.moduleContent .tablesorter tbody tr')
    for item in li:
        exc = {
            "nation" : list(item)[1].text,
            "value" : list(item)[3].text
        }
        excs.append(exc)
    print(excs)
    n=len(excs)

    return render_template('exchange.html', excs = excs, n=n)