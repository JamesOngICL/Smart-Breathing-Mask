
import smbus2					#import SMBus module of I2C
from time import sleep          #import
import json
import time


import json

import time

import threading

#some MPU6050 Registers and their Address
bus = smbus2.SMBus(1)

class temp_hum_sensor():
    '''
    
    A class to measure the temperature and humidity of the surrounding environment 

    '''

    def __init__(self):
        '''

        Constructor to initialize the temperature and humidity sensor and get the relevant 

        Attributes:
        temp_val -> 

        '''
        self.unconverted_temp = None
        self.hum_value = None

        pass


    def conv_temperature(self):
        """

        Converts the temperature value to relevant float format
        
        Inputs:
        type(class) self with all member attributes

        Output:
        convert_temp type(float) -> representing temperature converted to float

        """
        #temperature conv func
        convert_temp = (175.72*self.unconverted_temp)/65536
        convert_temp -= 46.85

        return convert_temp

    def conv_humidity(self,value):

        """

        Reads the humidity byte value and converts to float.

        Inputs:
        self, value

        Output:
        conv_humidity type(float) -> representing humidity converted to float

        """

        #humidity mapping function
        conv_humidity = 125*self.hum_value/65536
        conv_humidity -= 6

        return conv_humidity


    def read_temp_hum(self,mode):
        """

        Has an effect of reading temperature values from the sensor

        Inputs:
        type(class)-> self, type(str) -> mode corresponding to whether reading temperature or humidity

        Output:
        value -> type(float) representing converted temperature or humidity value. 

        """

        operation = {'temp':0xE3,'hum':0xE5}

        si7021_ADD = 0x40 #Add the I2C bus address for the sensor here
        si7021_READ_TEMPERATURE = operation[mode] #Add the command to read temperature here

        # bus = smbus2.SMBus(1)

        #Set up a write transaction that sends the command to measure temperature
        with threading.Lock():
            cmd_meas_temp = smbus2.i2c_msg.write(si7021_ADD,[si7021_READ_TEMPERATURE])

            #Set up a read transaction that reads two bytes of data
            read_result = smbus2.i2c_msg.read(si7021_ADD,2)

            #Execute the two transactions with a small delay between them
            bus.i2c_rdwr(cmd_meas_temp)
            time.sleep(0.1)
            bus.i2c_rdwr(read_result)
            print("OPENED threading lock")

        #convert the result to an int

        reading = int.from_bytes(read_result.buf[0]+read_result.buf[1],'big')

        #writes and initalizes the temperature and humidity sensors. 
        if mode=="temp":
            self.unconverted_temp = reading
            value = self.conv_temperature()
        else:
            self.hum_value = reading
            value = self.conv_humidity(reading)

        print("Get reading temp_sensor ", value)

        return value


