import sqlite3

def updatedevices(username,device):
      data = sqlite3.connect("devicedata.sqlite3")
      cmd = data.cursor()
      device = "'"+device+"'"
      username = "'"+username+"'"
      devicefound = cmd.execute("SELECT * FROM devicelist WHERE device="+device)
      devicefound = devicefound.fetchall()
      
      if len(devicefound)==0:
            return 0
      
      cmd.execute("""UPDATE devicelist SET username="""+username+""" WHERE device="""+device+";")
      data.commit()
      data.close()
      
      return 1

def getdevices(username):
      data = sqlite3.connect("devicedata.sqlite3")
      cmd = data.cursor()
      username = "'"+username+"'"
      devices = cmd.execute("SELECT device, model FROM devicelist WHERE username="+username)
      devices = devices.fetchall()       
      data.close()
      return devices

def updatereading(device,column,value):
      data = sqlite3.connect("devicedata.sqlite3")
      cmd = data.cursor()
      device = "'"+device+"'"
      devicefound = cmd.execute("SELECT * FROM devicelist WHERE device="+device)
      devicefound = devicefound.fetchall()
      
      if len(devicefound)==0:
            return 0
      
      cmd.execute("""UPDATE devicelist SET """+column+"""="""+str(value)+""" WHERE device="""+device)
      data.commit()
      data.close()
      
      return 1

def getreading(device,column):
      data = sqlite3.connect("devicedata.sqlite3")
      cmd = data.cursor()
      device = "'"+device+"'"
      devices = cmd.execute("""SELECT """+column+""" FROM devicelist WHERE device="""+device)
      readings = devices.fetchall()       
      data.close()
      return readings[0][0]

print(updatedevices("matthewsetiawan","MS3120001"))
print(getdevices("matthewsetiawan"))
print(updatereading("MS3120001","temperaturereading",5))
print(getreading("MS3120001","temperaturereading"))