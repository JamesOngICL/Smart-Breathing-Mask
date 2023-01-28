import sqlite3

def getimage(username):
      "Return image in this function"
      return 0

def getbalance(username):
      "Return balance in this function"
      return 0

def updatebalance(username, balanceamount):
      "Update balance in this function"
      return 0

def updatepassword(username, newpassword):
      return 0

def getabout(username):
      data = sqlite3.connect("data.sqlite3")
      cmd = data.cursor()
      username = "'"+username+"'"
      aboutme = cmd.execute("SELECT about FROM aboutme WHERE username="+username)
      dat = aboutme.fetchall()
      if len(dat)<1:
            cmd.execute("""INSERT INTO aboutme VALUES ("""+username+""",'');""")
            data.commit()
            aboutme = ""
      else:
            aboutme = dat[0][0]
      data.close()
      return aboutme

def updateabout(username,aboutme):
      data = sqlite3.connect("data.sqlite3")
      cmd = data.cursor()
      aboutme = "'"+aboutme+"'"
      username = "'"+username+"'"
      cmd1 = """UPDATE aboutme SET about="""+aboutme+""" WHERE username="""+username+";"
      cmd.execute("""UPDATE aboutme SET about="""+aboutme+""" WHERE username="""+username+";")
      data.commit()
      data.close()
      
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