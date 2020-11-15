# ------------------------------------------
# --- Author: Pradeep Singh
# --- Date: 20th January 2017
# --- Version: 1.0
# --- Python Ver: 2.7
# --- Details At: https://iotbytes.wordpress.com/store-mqtt-data-from-sensors-into-sql-database/
# ------------------------------------------
import datetime

from pymongo import MongoClient
import json

client = MongoClient(
    'mongodb+srv://admin:3qO8IPfPcuoXphGT@cluster0.2jeys.mongodb.net/cloud?retryWrites=true&w=majority')

db = client.mqtt

sensors = db['sensors'].find({'topic': 'ShopTraffic'})


def shop_traffic_handler(json_data):
    json_dict = json.loads(json_data)
    json_dict['date'] = datetime.datetime.strptime(json_dict['date'], "%d-%m-%Y %H:%M:%S")

    db.shop_traffic.insert_one(json_dict)


def sensor_data_handler(topic, json_data):
    if topic == "Home/WalawenderWedzicha/ShopTraffic":
        shop_traffic_handler(json_data)
