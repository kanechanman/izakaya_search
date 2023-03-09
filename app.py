from flask import Flask, render_template, request
import json
import requests
import urllib.parse
import pandas as pd
import os
import random


TEMPLATE_DIR = os.path.abspath('./templates')
STATIC_DIR = os.path.abspath('./static')
app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)

             
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

def HotpepperAPI(lat, lng, free_drink, code):
    api_key="42a14be89ba51a23" 
    if code:
        api = "http://webservice.recruit.co.jp/hotpepper/gourmet/v1/?" \
                "key={key}&lat={lat}&lng={lng}&budget={code}&free_drink={free_drink}&range=3&count=200&order=1&format=json"
    else:
        api = "http://webservice.recruit.co.jp/hotpepper/gourmet/v1/?" \
                "key={key}&lat={lat}&lng={lng}&free_drink={free_drink}&range=3&count=200&order=1&format=json"
    url=api.format(key=api_key,lat=lat, lng=lng, code=code, free_drink=free_drink)
    response = requests.get(url)
    result_list = json.loads(response.text)['results']['shop']
    shop_datas=[]
    for shop_data in result_list:
        shop_datas.append([shop_data["name"],shop_data["address"],shop_data["urls"]['pc'],shop_data["free_drink"], shop_data["budget"]['average'],shop_data["open"]])
    shop_datas = random.sample(shop_datas, 3)
    return shop_datas



@app.route('/', methods=["GET"])
def main_page():
    return render_template("templates.html")


@app.route("/results", methods=["POST"])
def result_page():
    pref = request.form["pref"]
    station = request.form["station"]
    
    #飲み放題設定
    drink = request.form.get("drink")
    if drink == "ari":
        free_drink = 1
    elif drink == "nasi":
        free_drink = 0
    #予算設定
    yosan = request.form.get("yosan")
    if yosan == "yosan0":
        code = None
    elif yosan == "B011":
        code = "B011"
    elif yosan == "B001":
        code = "B001"
    elif yosan == "B002":
        code = "B002"
    elif yosan == "B003":
        code = "B003"
    elif yosan == "B008":
        code = "B008"
    elif yosan == "B004":
        code = "B004"
    lat_st, lng_st = RailAPI(station, pref)
    shop_data = HotpepperAPI(lat_st, lng_st, free_drink, code)
    shop1 = shop_data[0]
    shop2 = shop_data[1]
    shop3 = shop_data[2]
    return render_template("search.html", shop1=shop1, shop2=shop2, shop3=shop3)



if __name__ == "__main__":
    app.run(port=8888) 