import sqlite3
import openai

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

def getmodel(device):
      data = sqlite3.connect("devicedata.sqlite3")
      cmd = data.cursor()
      device = "'"+device+"'"
      devices = cmd.execute("""SELECT model FROM devicelist WHERE device="""+device)
      readings = devices.fetchall()       
      data.close()
      return readings[0][0]

def getsensors(model):
      if model=="1.0 Temperature Scanner":
            return ["temperaturereading"]
      return []

def aiquery(query):
      # Set up the OpenAI API client
      openai.api_key = "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"
      # Set up the model and prompt
      model_engine = "text-davinci-002"
      prompt = "as a "+query+" tell me how to manage health in a few sentences, don't use however"

      # Generate a responseop
      completion = openai.Completion.create(
      engine=model_engine,
      prompt=prompt,
      max_tokens=1024,
      n=1,
      stop=None,
      temperature=0.5,
      )

      response = completion.choices[0].text
      
      return response

print(aiquery("consultant at BCG"))