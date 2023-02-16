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
* Video demonstrating the functioning of the product - script is available here: https://imperiallondon-my.sharepoint.com/:w:/g/personal/mzp20_ic_ac_uk/EfugM0uc02JAo0X8RFixDqABNL0SZZwlMIuWukn8jrV1zg?e=lh35id


## Tasks

* Multithreading - in progress - James
* Setting up air quality sensor - Milan
* Setting up marketing website - Milan
* Video script ready by Friday evening - Milan
* Reorganising code in an OOP way - Milan
* Setting up LED functionality - def led(state, color) - Milan

## Aims


## Contributors
Matthew Setiawan, Omar Zeidan, James Ong, Milan Paczai
<h2>Running the Server</h2>
<b>To run server locally:</b><br>
  python3 manage.py runserver<br><br>
<b>To run server on specified port:</b><br>
  python3 manage.py runserver 8000 <- port number<br><br>
<b>To run server on local internet for raspberry communications:</b><br>
  python3 manage.py runserver 0.0.0.0:8000 <- port number can be changed<br>
  #Then check your assigned ip to acess it using ipconfig, etc...<br><br>
 

