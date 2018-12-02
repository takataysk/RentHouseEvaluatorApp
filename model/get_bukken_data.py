from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
from pandas import Series, DataFrame
import time
import re

#データ取得
url = "https://suumo.jp/sp/chintai/osaka/ek/?e%5B%5D=206004641&e%5B%5D=206027220&e%5B%5D=206018460&e%5B%5D=206010230&e%5B%5D=206021790&e%5B%5D=206024550&e%5B%5D=206038670&e%5B%5D=206029250&e%5B%5D=206018500&e%5B%5D=206000950&e%5B%5D=206006590&e%5B%5D=206036290&e%5B%5D=206041520&e%5B%5D=206005210&e%5B%5D=206008070&e%5B%5D=206016820"
result = requests.get(url)
content = result.content

#HTMLを元に、オブジェクトを作る
soup = BeautifulSoup(content, 'html.parser')

#ページ数を取得
page_num = soup.find(id="totalPage").text
page_num = int(page_num)

#URLを入れるリスト
urls = []

#1ページ目を格納
urls.append(url)

#2ページ目から最後のページまでのURLを格納(URLの末尾のpage=XXXが変わる)
for i in range(page_num-1):
    pg = str(i+2)
    url_page = url + '&page=' + pg
    urls.append(url_page)

name = [] #マンション名
address = [] #住所
station = [] #最寄駅
toho = [] #駅徒歩~分
age = [] #築年数
height = [] #建物高さ
floor = [] #階
rent = [] #賃料
admin = [] #管理費
shikikin = [] #敷金
reikin = [] #礼金
floor_plan = [] #間取り
area = [] #専有面積
all_data = [] #全データ
#各ページで以下の動作をループ
count = 0

for url in urls:
    #物件リストを切り出し
    result = requests.get(url)
    content = result.content
    soup = BeautifulSoup(content, 'html.parser')
    toulist = soup.find_all("div", class_="toulistitem")

    if isinstance(toulist,type(None)):
        continue
    #各toulistに対し、以下の動作をループ
    for i in range(len(toulist)):
        
        #各建物から売りに出ている部屋数を取得
        #家賃のリスト
        toulistitem_sublist1 = toulist[i].find_all(class_='toulistitem_sublistitembody-descstrong-text1')
        #管理費のリスト
        toulistitem_sublist3 = toulist[i].find_all(class_='toulistitem_sublistitembody-descstrong-text3')
        #敷金礼金のリスト
        hiyou = toulist[i].find_all('dl', class_="toulistitem_sublistitembody-dllist")
        #その他（間取り、面積、階）のリスト
        others = toulist[i].find_all(class_='toulistitem_sublistitembody-desc')
        
        
        #マンション名取得
        subtitle = toulist[i].find(class_='toulistitem-inner-title').text
        
        #住所取得
        subaddress = toulist[i].find(class_='toulistitem_media-body').text
        subaddress = str(subaddress)
        subaddress = subaddress.replace('\t', '')
        subaddress = subaddress.replace('\xa0', '')
        subaddress = [i for i in re.split(r'\n',subaddress) if i != '']
        #最寄駅、最寄からの徒歩分、築年数、階数を取得
        eki = subaddress[0].split('/')[1].split(' ')[0]
        ekitoho = subaddress[0].split('/')[1].split(' ')[1]
        chikunen = subaddress[1].split('/')[0]
        takasa = subaddress[1].split('/')[1]
        #1つの物件の売りに出ている部屋数分繰り返す
        hiyou_count = 0
        for y in range(len(toulistitem_sublist1)):
            name.append(subtitle)
            address.append(subaddress[2])
            station.append(eki)
            toho.append(ekitoho)
            age.append(chikunen)
            height.append(takasa)
            #家賃の取得
            yachin = toulistitem_sublist1[y].text
            yachin = str(yachin)
            rent.append(yachin)
            #管理費の取得
            kanrihi = toulistitem_sublist3[y].text
            kanrihi = str(kanrihi)
            kanrihi = kanrihi.replace('\t', '')
            kanrihi = kanrihi.replace('\n(管理費\xa0', '')
            kanrihi = kanrihi.replace(')\n', '')
            admin.append(kanrihi)
            #敷金/礼金の取得
            shiki = hiyou[hiyou_count].find("dd").text
            shikikin.append(shiki)
            hiyou_count += 1
            rei = hiyou[hiyou_count].find("dd").text
            reikin.append(rei)
            hiyou_count += 1
            other = str(others[y].text)
            other = other.replace('\t', '')
            other = other.replace('\xa0', '')
            other = other.replace('/', '')
            other = [i for i in re.split(r'\n',other) if i != '']
            #間取り/占有面積/部屋の階数を取得
            floor_plan.append(other[0])
            area.append(other[1])
            floor.append(other[2])
    
    #プログラムを1秒間停止する（スクレイピングマナー）
    time.sleep(1)

    count += 1

    print(str(count) + 'ページ終了 / 全' + str(len(urls)) + 'ページ')

#各リストをシリーズ化
name = Series(name) #マンション名
address = Series(address)  #住所
station = Series(station) #最寄駅
toho = Series(toho) #駅徒歩~分
age = Series(age) #築年数
height = Series(height) #建物高さ
floor = Series(floor) #階
rent = Series(rent) #賃料
admin = Series(admin) #管理費
shikikin = Series(shikikin) #敷金
reikin = Series(reikin) #礼金
floor_plan = Series(floor_plan) #間取り
area = Series(area) #専有面積

#各シリーズをデータフレーム化
suumo_df = pd.concat([name, address, station, toho, age, height, floor, rent, admin, shikikin, reikin, floor_plan, area], axis=1)

#カラム名
suumo_df.columns=['マンション名','住所','最寄駅', '駅徒歩', '築年数','建物高さ','階','賃料','管理費', '敷金', '礼金', '間取り','専有面積']

#csvファイルとして保存
suumo_df.to_csv('./csv/bukken_kobeline.csv', sep = ',',encoding='utf-16')  

    
