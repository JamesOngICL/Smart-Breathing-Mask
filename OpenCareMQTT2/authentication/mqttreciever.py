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
                        print(tmp[i])
                        new_data = tmp[i][1:-2].split(",")
                        
                        print(float(new_data[0]))
                        print(float(new_data[1]))
                        print(float(new_data[2]))
                        val = (float(new_data[0])**2 + float(new_data[1])**2 + float(new_data[2])**2)**0.5
                  elif n[1]=="co2reading":
                        val = tmp[i]
                  elif n[1]=="heartratereading":
                        val = tmp[i]
                  extfunctions.updatereading(tmp["address"],n[1],val)

def on_message(client, userdata, message):
      print("received message: " , str(message.payload.decode("utf-8")))

      #Execute this upon recieving message
      file = open("mqttmessages.txt","w")
      file.write(str(message.payload.decode("utf-8")) + '\n')
      file.close()
      updatereadingmqtt(str(message.payload.decode("utf-8")))

mqttBroker = "146.169.217.129" 
client = mqtt.Client('webserver')
client.connect(mqttBroker, port=1883) 
client.subscribe("sensors/omar/readings")

client.on_message=on_message