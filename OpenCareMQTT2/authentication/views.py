from contextlib import _RedirectStream
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
import django.http
import extfunctions
import sqlite3
import authentication
import random
from django.http import JsonResponse
import rsa
from authentication import mqttreciever
from authentication.machinelearningmodel import DTree
import pickle
import numpy.core.multiarray

class DTree():
    def __init__(self):
        self.max_depth = 8
        self.left = None
        self.right = None
        self.leaf_val= None
        self.threshval = 1
        self.update_cols = -1

    def get_dict(self,input_vals):
        make_dict = {}
        for entry in input_vals:
            probability = 1.0/float(len(input_vals))
            if entry not in make_dict:
                make_dict[entry] = probability
            else:
                tmp = make_dict[entry]
                make_dict[entry] = tmp+probability
        return make_dict
    def eval_decision_tree(self,field_val):
        if self.leaf_val is not None:
            return self.leaf_val
        
        elif field_val[self.update_cols]>self.threshval:
            return self.right.eval_decision_tree(field_val)
        else:
            return self.left.eval_decision_tree(field_val)

def username_exists(username):
    if User.objects.filter(username=username).exists():
        return True
    return False

def chart(request):
      return render(request,"authentication/chart.html")

def livechart(request,id):
      devices = extfunctions.getdevices(request.user.username)
      found = 0
      if len(devices)>0:
            for i in range(len(devices)):
                  if id==devices[i][0]:
                        found = 1
                        break
      
      if found == 1: 
            return render(request,"authentication/chart.html",{"id":id})
      else:
            return yourdata(request)

def fetch_values(request):
      sensors = extfunctions.getsensors(extfunctions.getmodel(request.GET["id"]))
      print(request.GET)
      
      #Load ML Model
      picklefile = open('mydtree.pkl', 'rb')
      tree_obj = pickle.load(picklefile)
      picklefile.close()
      get_tree = tree_obj['dtree1']
      data = {}
      try: 
            data["condition"]=int(get_tree.eval_decision_tree([int(request.GET["hr"]),int(float(request.GET["energylevel"]))]))
      except:
            try:
                  data["condition"]=request.GET["prevcondition"]
            except:
                  data["condition"]=1
      for i in sensors:
            data[i] = extfunctions.getreading(request.GET["id"],i)
      return JsonResponse(data)

def keyreq(request):
      return JsonResponse({'key':str(mqttreciever.publicKey)})

def home(request):
      if request.method == "POST":
            tmp = dict(request.POST)
            for i in request.POST:
                  n = i.split(":")
                  if len(n)>1:
                        print("param:",tmp["address"][0],tmp[i],n[1])
                        val = ""
                        if n[1]=="temperaturereading":
                              val = tmp[i][0]
                        elif n[1]=="accelerometerreading":
                              val = (float(tmp[i][0])**2 + float(tmp[i][1])**2 + float(tmp[i][2])**2)**0.5
                        elif n[1]=="co2reading":
                              val = tmp[i][0]
                        elif n[1]=="heartratereading":
                              val = tmp[i][0]
                        extfunctions.updatereading(tmp["address"][0],n[1],val)
      return render(request, "authentication/index.html")

def signup(request):
      if request.method == "POST":
            username = request.POST['username']#name of the input tag
            fname = request.POST['firstname']
            lname = request.POST['lastname']
            email = request.POST['email']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            
            if User.objects.filter(username = username).exists():
                  return render(request, "authentication/signup.html")
            
            myuser = User.objects.create_user(username, email, password1)
            myuser.first_name = fname
            myuser.last_name = lname
            
            myuser.save()
            
            messages.success(request, "Your account has been sucessfully created!")
            
            return redirect("/signin")
      
      return render(request, "authentication/signup.html")

def signin(request):
      if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            
            user = authenticate(username=username, password=password)
            
            if user is not None:
                  login(request, user)
                  fname = user.first_name
                  return yourdata(request)
            
            else:
                  messages.error(request, "Bad Credentials")
                  return render(request, "authentication/signin.html")
            
      return render(request, "authentication/signin.html")

def homepage(request):
      return render(request, "authentication/index.html")

def profile(request):
      devices = extfunctions.getdevices(request.user.username)
      tempdevices = ""
      for i in range(len(devices)):
            tempdevices = tempdevices + devices[i][1] + ","
      return render(request, "authentication/profile.html",{'aboutme':extfunctions.getabout(request.user.username),'devices':tempdevices})

def profileedit(request):
      devices = extfunctions.getdevices(request.user.username)
      tempdevices = ""
      devicelist = []
      for i in range(len(devices)):
            tempdevices = tempdevices + devices[i][1] + ","
            devicelist.append(devices[i][0])
      if request.method == "POST":
            if "remove" in request.POST:
                  extfunctions.updatedevices("",devicelist[int(request.POST["remove"])])
            elif request.POST["newdevice"]!='':
                  extfunctions.updatedevices(request.user.username,request.POST["newdevice"])
            else:
                  extfunctions.updateabout(request.user.username,request.POST['aboutme'])
                  return profile(request)
      devices = extfunctions.getdevices(request.user.username)
      tempdevices = ""
      for i in range(len(devices)):
            tempdevices = tempdevices + devices[i][1]+","
      return render(request, "authentication/profileedit.html",{'aboutme':extfunctions.getabout(request.user.username),'devices':tempdevices})

def signout(request):
      logout(request)
      messages.success(request, "Logged Out Sucessfully")
      return home(request)

def yourdata(request):
      devices = extfunctions.getdevices(request.user.username)
      steps = ""
      tempdevices = ""
      for i in range(len(devices)):
            tempdevices = tempdevices + devices[i][1]+" ("+devices[i][0]+")"+","
            steps = steps + extfunctions.getreading(devices[i][0],"dailystep") + ","
      about = extfunctions.getabout(request.user.username)
      return render(request, "authentication/yourdata.html",{'aboutme':extfunctions.getabout(request.user.username),'devices':tempdevices,'aiquery':extfunctions.aiquery(about),'steps':steps})

def favorites(request):
      return render(request, "authentication/favorites.html")

def search(request):
      if request.method == "POST":
            usernamequery = request.POST["search"]
            if username_exists(usernamequery):
                  user = User.objects.get(username = usernamequery)
                  return render(request, "authentication/otherprofile.html",{'ousername':user.username,'ofirst_name':user.first_name,'olast_name':user.last_name,'oemail':user.email,'aboutme':extfunctions.getabout(user.username),'totsteps':totaldailysteps(user.username),'estburn':int(totaldailysteps(user.username)*0.04)})
            else:
                  print("not exists")
            print(request.POST["search"])
      return render(request, "authentication/search.html")

def totaldailysteps(username):
      devices = extfunctions.getdevices(username)
      steps = []
      for i in range(len(devices)):
            steps.append(int(extfunctions.getreading(devices[i][0],"dailystep")))
      return sum(steps)

def leaderboard(request):
      raw = extfunctions.leaderboard()
      data = ""
      for i in range(len(raw)):
            data = data + str(i+1) + ";" + str(raw[i][0]) + ";" + str(raw[i][1]) + ";" + str(int(int(raw[i][1])*0.04)) + ","
      return render(request, "authentication/leaderboard.html",{"data":data})