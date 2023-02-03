import sys
import requests
import http.client
import time
import math
import random

URL = 'http://127.0.0.1:8000'
track = 0

while(1):
    client = requests.session()
    # Retrieve the CSRF token first
    client.get(URL)  # sets cookie
    if 'csrftoken' in client.cookies:
        # Django 1.6 and up
        csrftoken = client.cookies['csrftoken']
    else:
        # older versions
        csrftoken = client.cookies['csrf']
    y = 5*math.sin((track/10)*16*3.14)+25
    login_data = {'Sensor:temperaturereading':str(y),'address':'MS3120001','csrfmiddlewaretoken':csrftoken}
    r = client.post(URL, data=login_data, headers=dict(Referer=URL))
    time.sleep(0.3)
    track = track + 0.3
    print(len(r.text))
    
