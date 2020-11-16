# ------------------------------------------
# --- Author: Pradeep Singh
# --- Date: 20th January 2017
# --- Version: 1.0
# --- Python Ver: 2.7
# --- Details At: https://iotbytes.wordpress.com/store-mqtt-data-from-sensors-into-sql-database/
# ------------------------------------------


import paho.mqtt.client as mqtt
import random
import threading
import json
from datetime import datetime

from shop import Shop

MQTT_Broker = "test.mosquitto.org"
MQTT_Port = 1883
Keep_Alive_Interval = 45
MQTT_Topic = "Home/WalawenderWedzicha/ShopTraffic"
current_people_quantity = 0
max_people_quantity = 3000


def on_connect(client, userdata, rc):
    if rc != 0:
        pass
        print("Unable to connect to MQTT Broker..." + ())
    else:
        print("Connected with MQTT Broker: " + str(MQTT_Broker))


def on_publish(client, userdata, mid):
    pass


def on_disconnect(client, userdata, rc):
    if rc != 0:
        pass


mqttc = mqtt.Client()
mqttc.on_connect = on_connect
mqttc.on_disconnect = on_disconnect
mqttc.on_publish = on_publish
mqttc.connect(MQTT_Broker, int(MQTT_Port), int(Keep_Alive_Interval))


def publish_to_topic(topic, message):
    mqttc.publish(topic, message)
    print(("Published: " + str(message) + " " + "on MQTT Topic: " + str(topic)))
    print("")


def publish_fake_sensor_values_to_mqtt():
    global current_people_quantity
    global max_people_quantity

    people_entered = random.randint(0, 100)
    while max_people_quantity - current_people_quantity - people_entered < 0:
        people_entered = random.randint(0, 100)
    people_left = random.randint(0, 100)
    while current_people_quantity - people_left < 0:
        people_left = random.randint(0, 100)

    current_people_quantity = current_people_quantity - people_left + people_entered

    threading.Timer(3.0, publish_fake_sensor_values_to_mqtt).start()

    publish_data = {'sensor_id': 1, 'shop_id': 1, 'date': (datetime.now()).strftime("%d-%m-%Y %H:%M:%S"),
                    'people_entered': people_entered, 'people_left': people_left,
                    'current_people_quantity': current_people_quantity}
    publish_json_data = json.dumps(publish_data)

    print(
        f"Publishing fake people traffic...\nEntered:{people_entered}\nLeft:{people_left}\nCurrent quantity:{current_people_quantity}")
    publish_to_topic(MQTT_Topic, publish_json_data)


if __name__ == "__main__":
    publish_fake_sensor_values_to_mqtt()
