import paho.mqtt.client as mqtt 
import time

client = mqtt.Client("Temperature_Sensor")
client.connect("localhost",port=1883)
login_data = {'Sensor:accelerometerreading':[1,2,3],'address':'MS3120001'}
MSG_INFO = client.publish("IC.embedded/jomp/test", str(login_data))
mqtt.error_string(MSG_INFO.rc)