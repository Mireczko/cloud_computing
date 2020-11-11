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

# ====================================================
# MQTT Settings
MQTT_Broker = "test.mosquitto.org"
MQTT_Port = 1883
Keep_Alive_Interval = 45
MQTT_Topic_Humidity = "Home/WalawenderWedzicha/Humidity"
MQTT_Topic_Temperature = "Home/WalawenderWedzicha/Temperature"


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


toggle = 0


def publish_fake_sensor_values_to_mqtt():
    threading.Timer(3.0, publish_fake_sensor_values_to_mqtt).start()
    global toggle

    if toggle == 0:
        humidity_fake_value = float("{0:.2f}".format(random.uniform(50, 100)))

        humidity_data = {'Sensor_ID': "Zamioculcas", 'Date': (datetime.today()).strftime(
            "%d-%m-%Y %H:%M:%S"), 'Humidity': humidity_fake_value}
        humidity_json_data = json.dumps(humidity_data)

        print("Publishing fake Humidity Value: " +
              str(humidity_fake_value) + "...")
        publish_to_topic(MQTT_Topic_Humidity, humidity_json_data)
        toggle = 1

    else:
        temperature_fake_value = float("{0:.2f}".format(random.uniform(1, 30)))

        temperature_data = {'Sensor_ID': "Zamioculcas", 'Date': (
            datetime.today()).strftime("%d-%m-%Y %H:%M:%S"), 'Temperature': temperature_fake_value}
        temperature_json_data = json.dumps(temperature_data)

        print("Publishing fake Temperature Value: " +
              str(temperature_fake_value) + "...")
        publish_to_topic(MQTT_Topic_Temperature, temperature_json_data)
        toggle = 0


if __name__ == "__main__":
    publish_fake_sensor_values_to_mqtt()
