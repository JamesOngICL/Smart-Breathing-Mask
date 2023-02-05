import time
import math
import paho.mqtt.client as mqtt 

track = 0

while(1):
    print("Sending...")
    client = mqtt.Client()
    client.connect("localhost",port=1883)
    y = 5*math.sin((track/10)*16*3.14)+25
    login_data = {'Sensor:temperaturereading':str(y),'address':'MS3120001'}
    MSG_INFO = client.publish("sensors/omar/temp", str(login_data))
    mqtt.error_string(MSG_INFO.rc)
    time.sleep(0.3)
    track = track + 0.3
    
