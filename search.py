# libraryをimport
import json
import requests
import urllib.parse
import pandas as pd

# 駅名・県名をinput
station ='栄'
pref='愛知県'

# Rail APIを使って駅名・県名から駅の緯度・経度を取得
def RailAPI(station, pref):
    station_url =urllib.parse.quote(station)
    pref_url =urllib.parse.quote(pref)
    api='http://express.heartrails.com/api/json?method=getStations&name={station_name}&prefecture={pref_name}'
    url=api.format(station_name=station_url, pref_name=pref_url)
    response=requests.get(url)
    result_list = json.loads(response.text)['response']['station']
    lng=result_list[0]['x']
    lat=result_list[0]['y']
    return lat, lng

lat_st, lng_st =RailAPI(station, pref)


# HotpepperAPIを使って駅の緯度・経度から飲み屋の情報を取得
def HotpepperAPI(lat, lng):
    api_key="42a14be89ba51a23" #自身で取得したAPI keyを入力
    api = "http://webservice.recruit.co.jp/hotpepper/gourmet/v1/?" \
            "key={key}&lat={lat}&lng={lng}&free_drink=1&private_room=1&course=1range=2&count=100&order=1&format=json"
    url=api.format(key=api_key,lat=lat_st, lng=lng_st)
    response = requests.get(url)
    result_list = json.loads(response.text)['results']['shop']
    shop_datas=[]
    for shop_data in result_list:
        shop_datas.append([shop_data["name"],shop_data["address"],shop_data["urls"]['pc'], shop_data["budget"]['average'], 'Hotpepper'])
    return shop_datas

columns = ['name','address', 'url', 'budget', 'source']
HP_data =pd.DataFrame(HotpepperAPI(lat_st, lng_st), columns=columns)

"""
# ぐるなびAPIを使って駅の緯度・経度から飲み屋の情報を取得
def GurunaviAPI(lat, lng):
    api_key=""　#自身で取得したAPI keyを入力
    api = "https://api.gnavi.co.jp/RestSearchAPI/v3/?" 
            "keyid={key}&latitude={lat}&longitude={lng}&range=2&private_room=1&bottomless_cup=1&hit_per_page=100"
    url=api.format(key=api_key,lat=lat_st, lng=lng_st)
    response = requests.get(url)
    result_list = json.loads(response.text)['rest']
    shop_datas=[]
    for shop_data in result_list:
        shop_datas.append([shop_data["name"],shop_data["address"],shop_data["url"], shop_data["budget"], "ぐるなび"])
    return shop_datas

columns = ['name', 'address', 'url', 'budget', 'source']
G_data =pd.DataFrame(GurunaviAPI(lat_st, lng_st), columns=columns)
"""

# HotpepperAPIとぐるなびAPIのデータを統合
#total_data=pd.concat([G_data, HP_data])
print(HP_data)