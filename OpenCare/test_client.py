import paho.mqtt.client as mqtt 
import time

client = mqtt.Client("Temperature_Sensor")
client.connect("test.mosquitto.org",port=1883)

MSG_INFO = client.publish("IC.embedded/jomp/test", "hello")
mqtt.error_string(MSG_INFO.rc)