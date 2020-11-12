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

tempSensors = db['sensors'].find({'topic': 'Temperature'})


def temp_handler(json_data):
    json_dict = json.loads(json_data)
    sensor_id = json_dict['Sensor_ID']
    data_and_time = data_and_time = datetime.datetime.strptime(json_dict['Date'], "%d-%m-%Y %H:%M:%S")
    temperature = json_dict['Temperature']
    to_save = {"sensorId": sensor_id,
               "date": data_and_time, "temp": temperature}

    db.temperature.insert_one(to_save)


def hum_handler(json_data):
    json_dict = json.loads(json_data)
    sensor_id = json_dict['Sensor_ID']
    data_and_time = datetime.datetime.strptime(json_dict['Date'], "%d-%m-%Y %H:%M:%S")
    humidity = json_dict['Humidity']
    to_save = {"sensorId": sensor_id,
               "date": data_and_time, "humidity": humidity}

    db.humidity.insert_one(to_save)


def acidity_handler(json_data):
    json_dict = json.loads(json_data)
    sensor_id = json_dict['Sensor_ID']
    data_and_time = data_and_time = datetime.datetime.strptime(json_dict['Date'], "%d-%m-%Y %H:%M:%S")
    acidity = json_dict['Acidity']
    to_save = {"sensorId": sensor_id,
               "date": data_and_time, "acidity": acidity}

    db.acidity.insert_one(to_save)


def sensor_data_handler(topic, json_data):
    if topic == "Home/WalawenderWedzicha/Temperature":
        temp_handler(json_data)
    elif topic == "Home/WalawenderWedzicha/Humidity":
        hum_handler(json_data)
    elif topic == "Home/BartekDawid/Acidity":
        acidity_handler(json_data)
