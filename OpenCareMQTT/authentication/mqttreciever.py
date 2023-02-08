import requests 
import paho.mqtt.client as mqtt
import time
import extfunctions
import ast

# calculate heart rate based on peaks recorded in graph
# create a buffer that stores the last 20 values of heart rate
# record te time between peaks 
# calculate the beats per minute using it
# update the heart rate in the database
def calculate_bpm(data, buffer_size=20):
    r_peaks = []
    buffer = []
    start_time = time.time()
    for i in range(len(data)):
        buffer.append((data[i], time.time() - start_time))
        if len(buffer) >= buffer_size:
            peak = max(buffer, key=lambda x: x[0])
            if peak[0] == data[i]:
                r_peaks.append(peak[1])
            buffer = []
    if len(r_peaks) < 2:
        return None
    time_diff = (r_peaks[-1] - r_peaks[0]) / len(r_peaks)
    bpm = 60 / time_diff
    return bpm


def updatereadingmqtt(message):
      tmp = ast.literal_eval(message)
      print("tmp is: ", tmp)
      for i in tmp:
            n = i.split(":")
            if len(n)>1:
                  print("param:",tmp["address"],tmp[i],n[1])
                  val = ""
                  if n[1]=="temperaturereading":
                        val = tmp[i]
                        # val = calculate_bpm(val)                        
                  elif n[1]=="heartratereading":
                        pass
                              
                  elif n[1]=="accelerometerreading":
                        print("vals")
                        print(tmp[i])
                        new_data = tmp[i][1:-2].split(",")
                        
                        print(float(new_data[0]))
                        print(float(new_data[1]))
                        print(float(new_data[2]))
                        val = (float(new_data[0])**2 + float(new_data[1])**2 + float(new_data[2])**2)**0.5
                  extfunctions.updatereading(tmp["address"],n[1],val)
                  

def on_message(client, userdata, message):
      print("received message: " , str(message.payload.decode("utf-8")))

      #Execute this upon recieving message
      file = open("mqttmessages.txt","w")
      file.write(str(message.payload.decode("utf-8")) + '\n')
      file.close()
      updatereadingmqtt(str(message.payload.decode("utf-8")))

mqttBroker = "146.169.217.129" #"146.169.217.129"
client = mqtt.Client('webserver')
client.connect(mqttBroker, port=1883) 
client.subscribe("sensors/omar/readings")

client.on_message=on_message