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
from datetime import datetime, timedelta

from shop import Shop

MQTT_Broker = "test.mosquitto.org"
MQTT_Port = 1883
Keep_Alive_Interval = 45
MQTT_Topic = "Home/WalawenderWedzicha/ShopTrafficLeft"
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


def publish_fake_sensor_values_to_mqtt():
    timer_value = random.randint(1, 20)
    print(f"timer{timer_value}")
    threading.Timer(timer_value, publish_fake_sensor_values_to_mqtt).start()

    publish_data = {'sensor_id': 2, 'shop_id': 1,
                    'date': (datetime.now() + timedelta(hours=1)).strftime("%d-%m-%Y %H:%M:%S")}
    publish_json_data = json.dumps(publish_data)

    print(
        f"Person entered the shop")
    publish_to_topic(MQTT_Topic, publish_json_data)


if __name__ == "__main__":
    publish_fake_sensor_values_to_mqtt()
