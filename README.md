# Project by Smart Team

This is a project for the 3rd Year EE Embedded Systems Module.

Project guide is available here: https://github.com/edstott/ES-CW1/blob/main/README.md

## Final Idea

The final idea was to develop a smart mask that can also be used as a wearable. It is ideal for doctors who are our target customers, as well as people who live in very polluted areas, where air quality is extremely variable. 

The product keeps track of their calories by measuring steps, heart rate through a PPG sensor, and also monitors the surrounding air quality using VOC and CO2 sensors. For the development of the product, we spoke to various doctors and engineers as well as conducting much of our own market research to prototype a product that could truly be used in the widespread commercial sector. Please refer to our marketing website to see the latest information about the mask and our marketing research.            


Marketing website: https://pmz7696.wixsite.com/opencare

## Github Organization

A total of 4 development branches were used to build the frontend of the website as well as program the hardware. The final folders OPENCAREMQTT and hardware_final contain the complete and finished code that our group used to demonstrate the project.     

## Running the hardware 

Please wire the 4 sensors according to documentation (with GPIO 23 and 24) used as the SCL and SDA pins for the CO2 sensor. Following this run this in the directory hardware_final.
````shell
pip3 install requirements.txt
````

````shell
python3 main.py 
````

# Running the Server
* Visit folder containing manage.py -> serverside_branch/OpenCareMQTT2/manage.py
<b>To run server locally:</b><br>
````shell
  python3 manage.py runserver
````
<b>To run server on specified port:</b><br>
````shell
  python3 manage.py runserver 8000 <- port number<br><br>
````
<b>To run server on local area network for raspberry communications:</b><br>
````shell
  python3 manage.py runserver 0.0.0.0:8000 #port number can be changed
    #Then check your assigned ip to acess it using ipconfig, etc...

````


## Contributors

Our group had a primarily flat structure with each member focusing on specific section for development and deployment. This provides a very brief description of the roles and contributions for each of the members in this group.   

Matthew Setiawan (Frontend), Omar Zeidan (Communications MQTT), James Ong (Hardware), Milan Paczai (Hardware) 

# Project Management

## Meeting Times

* Mondays: 11:30 AM
* Wednesdays: 10AM - 12PM
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

## Sensors Available

* accelerometer
* ppd sensor
* co2 sensor
* temperature and humidity sensor


## Other Electronic Components

* Raspberry Pi Zero


 

