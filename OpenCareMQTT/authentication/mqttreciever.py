import requests 
import paho.mqtt.client as mqtt
import time
import extfunctions
import ast

def updatereadingmqtt(message):
      tmp = ast.literal_eval(message)
      print(tmp)
      for i in tmp:
            n = i.split(":")
            if len(n)>1:
                  print("param:",tmp["address"],tmp[i],n[1])
                  val = ""
                  if n[1]=="temperaturereading":
                        val = tmp[i]
                  elif n[1]=="accelerometerreading":
                        print("vals")
                        print(float(tmp[i][0]))
                        print(float(tmp[i][0]))
                        print(float(tmp[i][0]))
                        val = (float(tmp[i][0])**2 + float(tmp[i][1])**2 + float(tmp[i][2])**2)**0.5
                  extfunctions.updatereading(tmp["address"],n[1],val)

def on_message(client, userdata, message):
      print("received message: " ,str(message.payload.decode("utf-8")))

      #Execute this upon recieving message
      file = open("mqttmessages.txt","w")
      file.write(str(message.payload.decode("utf-8")))
      file.close()
      updatereadingmqtt(str(message.payload.decode("utf-8")))

mqttBroker ="test.mosquitto.org"
client = mqtt.Client("Webserver")
client.connect(mqttBroker) 
client.subscribe("IC.embedded/jomp/test")

client.on_message=on_message 