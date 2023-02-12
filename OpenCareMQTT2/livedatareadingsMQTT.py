import time
import math
import paho.mqtt.client as mqtt 
import requests
import rsa
import binascii

track = 0

def getkey(url):
    key = requests.get(url)
    key = key.text.split(":")[1].split("}")[0].split('"')[1]
    key_components = key[len("PublicKey("):-1].split(", ")
    n = int(key_components[0])
    e = int(key_components[1])
    public_key = rsa.PublicKey(n, e)
    return public_key

def encrypt(message,key):
    return binascii.hexlify(rsa.encrypt(message.encode(),key)).decode()
    
key = getkey('http://127.0.0.1:8000/keyreq')

while(1):
    print("Sending...")
    client = mqtt.Client("Temperature_Sensor")
    client.connect("192.168.0.17",port=1883)
    y = 5*math.sin((track/10)*16*3.14)+25
    login_data = {'Sensor:heartratereading':str(y),'address':'MS3120001'}
    print(encrypt(str(login_data),key))
    MSG_INFO = client.publish("sensors/omar/readings", encrypt(str(login_data),key))
    mqtt.error_string(MSG_INFO.rc)
    time.sleep(0.3)
    track = track + 0.3

    
