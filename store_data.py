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

sensor_id = 1
shop_dict = {}
client = MongoClient(
    'mongodb+srv://admin:3qO8IPfPcuoXphGT@cluster0.2jeys.mongodb.net/cloud?retryWrites=true&w=majority')

db = client.mqtt

sensors = db['sensors'].find({'topic': 'ShopTraffic'})


def shop_traffic_handler_entered(json_data, state):
    global shop_dict
    global sensor_id
    json_dict = json.loads(json_data)
    if str(json_dict['shop_id']) not in shop_dict:
        shop_dict[str(json_dict['shop_id'])] = {'people_entered': 0, 'people_left': 0,
                                                'current_people_quantity': 0}
    if state:
        if shop_dict[str(json_dict['shop_id'])]['current_people_quantity'] < 300:
            shop_dict[str(json_dict['shop_id'])]['people_entered'] += 1
            shop_dict[str(json_dict['shop_id'])]['current_people_quantity'] += 1
    else:
        if shop_dict[str(json_dict['shop_id'])]['current_people_quantity'] > 0:
            shop_dict[str(json_dict['shop_id'])]['people_left'] += 1
            shop_dict[str(json_dict['shop_id'])]['current_people_quantity'] -= 1
    json_dict['date'] = datetime.datetime.strptime(json_dict['date'], "%d-%m-%Y %H:%M:%S")
    shop_dict[str(json_dict['shop_id'])]['date'] = json_dict['date']
    people_sum = shop_dict[str(json_dict['shop_id'])]['people_left'] + shop_dict[str(json_dict['shop_id'])]['people_entered']
    if people_sum >= 10:
        send_dict = shop_dict[str(json_dict['shop_id'])]
        send_dict['shop_id'] = json_dict['shop_id']
        new_dict = dict(send_dict)
        db.shop_traffic.insert_one(new_dict)
        shop_dict[str(json_dict['shop_id'])]['people_entered'] = 0
        shop_dict[str(json_dict['shop_id'])]['people_left'] = 0


def sensor_data_handler(topic, json_data):
    if topic == "Home/WalawenderWedzicha/ShopTrafficEntered":
        shop_traffic_handler_entered(json_data, 1)
    elif topic == "Home/WalawenderWedzicha/ShopTrafficLeft":
        shop_traffic_handler_entered(json_data, 0)
