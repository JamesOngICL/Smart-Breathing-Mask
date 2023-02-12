import time
import math
import paho.mqtt.client as mqtt 
import requests
import rsa
import binascii

track = 0

def getkey():
    public_key = rsa.PublicKey(17822536325291103101323819498187309223540366914795284790480275832907387155167793075777561150522889142593001669196266128814411559496746832319118549807122213726549864914547111915612810151458421841885576703978191424830064979840625261982526983948534265579315189645712708057829444744526097651478257973249834256433525747544157305555064689911278584472322809386995238704397789909958860784202773540915843232935732240372781175094908655965143500697948600899964661078620371137797175431929993230441845012688184755850715508366128027618816784376158765529688868977572400965001046656964586523083679277864216337830024186581266532501199, 65537)
    return public_key

def encrypt(message,key):
    return binascii.hexlify(rsa.encrypt(message.encode(),key)).decode()
    
key = getkey()

while(1):
    print("Sending...")
    client = mqtt.Client("Temperature_Sensor")
    client.connect("192.168.0.17",port=1883)
    y = 5*math.sin((track/5)*16*3.14)+20000
    login_data = {'Sensor:heartratereading':str(y),'address':'MS3120001'}
    print(encrypt(str(login_data),key))
    MSG_INFO = client.publish("sensors/omar/readings", encrypt(str(login_data),key))
    mqtt.error_string(MSG_INFO.rc)
    time.sleep(0.3)
    track = track + 0.3

    
