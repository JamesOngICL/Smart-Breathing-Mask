
import smbus2					#import SMBus module of I2C
from time import sleep          #import
import json
import time

import queue
import threading
import json
import random

import sys
import requests
import http.client
import time
import math
import random

bus = smbus2.SMBus(1)


class air_sensor():
    
    def __init__(self,address=0x5A):
        '''

        Initializes the Co2 sensor and other parameters to be used. On my raspberry pi I got the i2c address of 0x5A. Hence I used this parameter, 
        
        '''
        #CO2 sensor is default programmed to 0x5a on I2C bus. 
        self.addr = address
        self.app_reg = 0xF4
        self.reset_reg = 0xFF
        self.meas_mode = 0x01
        self.stat_reg = 0x00
        self.co2_air_qual = None



    def setup_co2_sensor(self):

        '''
        
        Method and means of initializing a carbon dioxide sensor. 
        
        '''
        print("Running Initializations")

        #Resetthe CO2 sensor
        bus.write_i2c_block_data(self.addr,self.reset_reg,[0x11,0xE5,0x72,0x8A])
        time.sleep(0.3)

        #write to the status register
        bus.write_byte_data(self.addr,self.stat_reg,1)

        #Writing to application register
        bus.write_i2c_block_data(self.addr,self.app_reg, [])
        time.sleep(0.3)

        # Set to 72 to increase sensor reading rate. See datasheet for justification. 
        bus.write_byte_data(self.addr,self.meas_mode,24)

        # print("working")
        time.sleep(0.3)
        print("Finished CO2 Initialization")

        return



    def get_air_params(self):

        ''' 

        Function to update the self.co2_air_qual parameter        

        '''

        #reads the eco2 parameters and VOC level
        value_read = 0

        #set a time limit of 12 seconds for readings to be produced
        read_duration = 12
        curr_time = time.time()
        elapse_time = 0

        while elapse_time<read_duration:

            #deduce the current time passed see if data available. 

            elapse_time = time.time()-curr_time
            read_status = bus.read_byte_data(self.addr,0x00)
            tmp = format(read_status,"#010b")[2:]
            time.sleep(0.5)

            #Control flow condition indicating that data is ready and avaialble
            if tmp[4]==str(1):

                co2_air_qual = bus.read_i2c_block_data(self.addr,0x02,4)
                print("Reading CO2 & Air Quality Levels",co2_air_qual)

                time.sleep(0.1)

                #update the co2 parameter stored in class object. 
                self.co2_air_qual = co2_air_qual

                #break and return
                return co2_air_qual

        print("no data available")

        return None


    def get_co2_vol_comp(self):
        '''

        Inputs (assuming no errors):
        type(array) -> self.co2_arr_qual
    

        Outputs (assuming no errors):
        type(array) -> co2_level and voc_level corresponding to ppm of C02 detectable from atmosphere and volatile organic compounds.  

        Notes:
        eco2 is in the first 2 bit fields of self.co2_air_qual.
        Perform an LSL (logical shift left from IAC) to get the relevant param ppb
        
        '''
        #Process co2 data and send this
        try:

            #get value params
            left_co2_val, right_co2_val = self.co2_air_qual[0],self.co2_air_qual[1]

            #gets the left_addr_val from CO2 sensor
            left_co2_val = left_co2_val<<8

            #aggregate the values to get co2_level
            co2_level = left_co2_val+right_co2_val

            #reads in a litle endian format. 
            left_voc, right_voc = self.co2_air_qual[2], self.co2_air_qual[3]

            #gets the volatile organic copound level
            voc_level = (left_voc<<8)+right_voc

            #returns the co2 and volatile organic compounds levels 
            return [co2_level,voc_level]

        except:
            return None

        


air_reader = air_sensor(0x5A)
curr_time = time.time()
elapse_time = 0

while elapse_time<45:
    print("TIME ELAPSED:",elapse_time)

    #Gets the air_params sensor readings.  
    air_reader.get_air_params()

    #Get the values of Co2 and volatile organics. 
    air_readings = air_reader.get_co2_vol_comp()

    #readings to be taken. 
    print(air_readings, "Note left is Co2 and right is volatile organic compounds")

    #Gets time elapsed. 
    elapse_time = time.time()-curr_time








