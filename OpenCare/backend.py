import requests 

import paho.mqtt.client as mqtt
import time

def on_message(client, userdata, message):
    print("received message: " ,str(message.payload.decode("utf-8")))

mqttBroker ="test.mosquitto.org"

client = mqtt.Client("Webserver")
client.connect(mqttBroker) 

client.loop_start()

client.subscribe("IC.embedded/jomp/test")
client.on_message=on_message 

time.sleep(30)
client.loop_stop()