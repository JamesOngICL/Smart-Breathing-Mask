import time
import math
import paho.mqtt.client as mqtt 

track = 0

while(1):
    print("Sending...")
    client = mqtt.Client("Temperature_Sensor")
    client.connect("test.mosquitto.org")
    y = 5*math.sin((track/10)*16*3.14)+25
    login_data = {'Sensor:heartratereading':str(y),'address':'MS3120001'}
    MSG_INFO = client.publish("IC.embedded/jomp/opencare", str(login_data))
    mqtt.error_string(MSG_INFO.rc)
    time.sleep(0.3)
    track = track + 0.3
    
