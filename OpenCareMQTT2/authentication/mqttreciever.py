import requests 
import paho.mqtt.client as mqtt
import time
import extfunctions
import ast
import socket
import rsa
import binascii

publicKey, privateKey = rsa.newkeys(2048)

def updatereadingmqtt(message):
      #Decrypt First
      message = binascii.unhexlify(message.encode())
      message = rsa.decrypt(message,privateKey).decode()
      
      tmp = ast.literal_eval(message)
      for i in tmp:
            n = i.split(":")
            if len(n)>1:
                  val = ""
                  if n[1]=="temperaturereading":
                        val = tmp[i]
                  elif n[1]=="accelerometerreading":
                        new_data = tmp[i][1:-2].split(",")
                        val = (float(new_data[0])**2 + float(new_data[1])**2 + float(new_data[2])**2)**0.5
                        extfunctions.updatesteps(tmp["address"],val,0.05)
                  elif n[1]=="co2reading":
                        new_data = tmp[i][1:-2].split(",")
                        val = new_data[0]
                  elif n[1]=="heartratereading":
                        val = tmp[i]
                  extfunctions.updatereading(tmp["address"],n[1],val)

def on_message(client, userdata, message):
      #Execute this upon recieving message
      updatereadingmqtt(message.payload.decode("utf-8"))

#Get IP automatically
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip = s.getsockname()[0]

mqttBroker = ip 
client = mqtt.Client('webserver')
client.connect(mqttBroker, port=1883) 
client.subscribe("sensors/omar/readings")

client.on_message=on_message