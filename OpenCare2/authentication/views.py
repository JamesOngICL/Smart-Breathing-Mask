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

# Create your views here.
def chart(request):
      return render(request,"authentication/chart.html")

def fetch_values(request):
      print("fetched")
      file = open("test.txt","r")
      val = float(file.read())
      file.close()
      data = {'result':val}
      return JsonResponse(data)

def home(request):
      if request.method == "POST":
            print(request.POST)
            file = open("test.txt","w")
            file.write(request.POST["temperature"])
            file.close()
      return render(request, "authentication/index.html")

def signup(request):
      if request.method == "POST":
            username = request.POST['username']#name of the input tag
            fname = request.POST['firstname']
            lname = request.POST['lastname']
            email = request.POST['email']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            
            myuser = User.objects.create_user(username, email, password1)
            myuser.first_name = fname
            myuser.last_name = lname
            
            myuser.save()
            
            messages.success(request, "Your account has been sucessfully created!")
            
            return redirect('signin')
      
      return render(request, "authentication/signup.html")

def signin(request):
      if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            
            user = authenticate(username=username, password=password)
            
            if user is not None:
                  login(request, user)
                  fname = user.first_name
                  return render(request, "authentication/index.html", {'firstname':fname})
            
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
            tempdevices = tempdevices + devices[i][1]+"("+devices[i][0]+")"+","
      print(tempdevices)
      return render(request, "authentication/profile.html",{'aboutme':extfunctions.getabout(request.user.username),'devices':tempdevices})

def profileedit(request):
      devices = extfunctions.getdevices(request.user.username)
      tempdevices = ""
      devicelist = []
      for i in range(len(devices)):
            tempdevices = tempdevices + devices[i][1]+"("+devices[i][0]+")"+","
            devicelist.append(devices[i][0])
      if request.method == "POST":
            print(request.POST)
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
            tempdevices = tempdevices + devices[i][1]+"("+devices[i][0]+")"+","
      return render(request, "authentication/profileedit.html",{'aboutme':extfunctions.getabout(request.user.username),'devices':tempdevices})

def signout(request):
      logout(request)
      messages.success(request, "Logged Out Sucessfully")
      return home(request)

def yourdata(request):
      return render(request, "authentication/yourdata.html",{'aboutme':extfunctions.getabout(request.user.username)})

def favorites(request):
      return render(request, "authentication/favorites.html",{'aboutme':extfunctions.getabout(request.user.username)})

def search(request):
      return render(request, "authentication/search.html",{'aboutme':extfunctions.getabout(request.user.username)})