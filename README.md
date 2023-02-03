# Project by the Smart Team

It's a project for the 3rd Year EE Embedded Systems Module.

Project guide is available here: https://github.com/edstott/ES-CW1/blob/main/README.md

## Final Idea

Smart mask that can also be used as a wearable. It is good for doctors, they are our target customers, as well as people who live in very polluted areas, where air quality can vary a lot. 

It keeps track of their calories by measuring steps, (heart rate?), while also monitoring the surrounding air quality. 


Marketing website: https://pmz7696.wixsite.com/opencare


## Ideas

* Smart Mailbox
* Smart Window
* Smart Gate
* Smart Nailpolish 
* Smart Doorflap
* Smart Device that 
* Smart Lie Detector

## Sensors Available

* accelerometer
* time of flight distance
* thermal pile (non contact temperature sensor)
* load cell (for sensor)
* air quality sensor
* adc for analog sensors
* atmospheric pressure sensor
* magnetometer (compass)
* spectual light sensor
* ultrasonic range finder
* flex sensor
* air temperature and humidity sensor
* air velocity sensor


## Other Electronic Components

* push button
* servomotor
* slide switch
* vibration motor
* LED
* Raspberry PI


# Project Management

## Meeting Times

* Mondays: (time to confirm!)
* Wednesdays: 10am - 12pm
* Friday: (time to confirm!)

## Timeline

* 23 Jan - Week 1: raspberry setup, idea finalised
* 30 Jan - Week 2: website setup, MVP in progress
* 6 Feb - Week 3: MVP Ready: Week 3 end 1 Feb (ie two weeks before deadline - confirm!), video produce
* 13 Feb - Week 4: Deadline: 15 Feb 

## Deliverables

* GitHub code that integrates sensor with platform and uploads data to servers 
* Website that markets the product
* Video demonstrating the functioning of the product


## Tasks

* Multithreading - in progress - James
* Setting up air quality sensor - Milan
* Setting up marketing website - Milan
* Video script ready by Friday evening - Milan
* Reorganising code in an OOP way - Milan
* Setting up LED functionality - def led(state, color) - Milan

## Aims


## Contributors
Frontend
<h2>Running the Server</h2>
<b>To run server locally:</b><br>
  python3 manage.py runserver<br><br>
<b>To run server on specified port:</b><br>
  python3 manage.py runserver 8000 <- port number<br><br>
<b>To run server on local internet for raspberry communications:</b><br>
  python3 manage.py runserver 0.0.0.0:8000 <- port number can be changed<br>
  #Then check your assigned ip to acess it using ipconfig, etc...<br><br>
  
<h2>Core Files</h2>
- extfunctions.py -> imported in views.py<br>
- authentication/views.py -> main backend code<br>
- authentication/urls.py -> link urls and functions in views.py<br>
- templates/authentication -> frontend html stuff<br>
  
<h2>Understanding the backend</h2>
The two important files are views.py and urls.py under authentication folder.<br><br>The only real backend files are under authentication/views.py where all the functions are, the file authentication/urls.py specifies which function should be associated with a specified url. The file extfunctions.py on the outside is imported in views.py to write functions more cleanly.

<h2>Understand the frontend</h2>
The important files for frontend is under templates/authentication. These files are acessed in views.py. We can pass parameters into these html files in views.py by doing something like this:<br><br>return render(request, "authentication/search.html",{'aboutme':extfunctions.getabout(request.user.username)})<br><br>Here this function will render search.html file for the user. The dictionary is passed and can be accessed in the html file. We can extract this data by simply writing {{aboutme}} in the html code.

<h2>Http requests</h2>
The main http request is under home() function in views.py. Try sending a post data using the python file and the data should be recieved by this function. You can try printing request.POST() and see that your JSON data has been received here.

<h2>Other files</h2>
Don't worry about most of the other unmentioned files, they are there by default and are usually not changed.
 
=======
main
