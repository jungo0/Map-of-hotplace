import pandas as pd
import time
from urllib.request import urlopen
from urllib import parse
from urllib.request import Request
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import urllib
import json
import numpy as np


client_id='7v4pfbruwz'
client_pw='ahsAA2dIcQuUo35b3G7uIWw0lm3gGKaXrXGcRTBd'

api_url="https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode?query="
df =  pd.read_csv('./음식점(반반).csv', encoding='cp949')

df=df[['소재지전체주소','사업장명','도로명전체주소']]

df['소재지전체주소']=df['소재지전체주소'].str.split(" ").str[2]
df['사업장명']=df['사업장명'].str.split("(").str[0]
df['사업장명']=df['사업장명'].str.split("[").str[0]


from selenium import webdriver


chromedriver = '/Users/datakim/workspace/selenium_learning/chromedriver'
driver = webdriver.Chrome(executable_path='chromedriver.exe')

df['kakao_keyword'] = df['소재지전체주소'] +" " + df['사업장명']
df['kakao_map_url'] = ''


star=[]
star_nums=[]
review=[]


for i, keyword in enumerate(df['kakao_keyword'].tolist()):
    print("이번에 찾을 키워드 :", i, f"/ {df.shape[0]} 행", keyword)
    try:
        kakao_map_search_url = f"https://map.kakao.com/?q={keyword}"
        driver.get(kakao_map_search_url)
        time.sleep(1)
        rate = driver.find_element_by_css_selector("#info\.search\.place\.list > li:nth-child(1) > div.rating.clickArea > span.score > em").text
        num =driver.find_element_by_css_selector("#info\.search\.place\.list > li:nth-child(1) > div.rating.clickArea > span.score > a").text
        rateNum = driver.find_element_by_css_selector("#info\.search\.place\.list > li:nth-child(1) > div.rating.clickArea > a > em").text
        print("리뷰" + rateNum + ", 평점 " + rate +", 별점사람수"+num)

    except Exception as e1:
        print("정보 없음")
        rate="삭제"
        num="삭제"
        rateNum="삭제"
        pass

    try:
        star.append(rate)
        star_nums.append(num)
        review.append(rateNum)
    except Exception as e2:
        pass



print(df)
geo_coordi=[]
for add in df['도로명전체주소']:
    add_urlenc=parse.quote(add)
    url=api_url+add_urlenc
    print(url)
    request=Request(url)
    request.add_header("X-NCP-APIGW-API-KEY-ID",client_id)
    request.add_header("X-NCP-APIGW-API-KEY",client_pw)
    try:
        response=urlopen(request)
    except HTTPError as e:
        print('HTTP Error!')
        latitude = None
        longitude = None

    else:
        rescode=response.getcode()
        if rescode == 200:
            response_body = response.read().decode('utf-8')
            response_body = json.loads(response_body)
            if 'addresses' in response_body:
                try:
                    latitude=response_body['addresses'][0]['y']
                    longitude=response_body['addresses'][0]['x']
                    print("success")
                except:
                    latitude=0
                    longitude=0
            else:
                print('result not exist')
                latitude=None
                longitude=None

        else:
            print("Response error code: %d" %rescode)
            latitude=None
            longitude=None

    geo_coordi.append([latitude,longitude])
print(response_body)
np_geo_coord=np.array(geo_coordi)
print(geo_coordi)
print(np_geo_coord)

df=pd.DataFrame({"소재지전체주소":df['소재지전체주소'].values,
                                "도로명전체주소":df['도로명전체주소'].values,
                                "사업장명":df['사업장명'].values,
                                "위도":np_geo_coord[:,0],
                                "경도":np_geo_coord[:,1],
                                "kakao_star":star,
                                "kakao_star_nums":star_nums,
                                "kakao_blog_review":review,
                                })
df['kakao_star_nums']=df['kakao_star_nums'].str.split("건").str[0]

df.to_csv("./음식점(반반).csv",index=False, sep=",",encoding='utf-8')