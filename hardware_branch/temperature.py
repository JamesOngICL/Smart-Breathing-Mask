
import smbus2					#import SMBus module of I2C
from time import sleep          #import
import json
import time


import json

import time

import threading_almost_fin as inh

#some MPU6050 Registers and their Address
class temp_hum_sensor():

    def __init__(self):
        pass


    def conv_temperature(self,value):
        """

        Converts the temperature value to relevant integer format

        """
        #temperature conv func
        temp = (175.72*value)/65536
        temp -= 46.85

        return temp

    def conv_humidity(self,value):

        """

        Reads the humidity byte value and converts to float.

        """

        #humidity mapping function
        humidity = 125*value/65536
        humidity -= 6

        return humidity


    def read_temp_hum(self,mode):
        """

        Has an effect of reading temperature values from the sensor

        """

        operation = {'temp':0xE3,'hum':0xE5}

        diff_time = time.time()
        si7021_ADD = 0x40 #Add the I2C bus address for the sensor here
        si7021_READ_TEMPERATURE = operation[mode] #Add the command to read temperature here

        # bus = smbus2.SMBus(1)

        #Set up a write transaction that sends the command to measure temperature
        with inh.lock:
            cmd_meas_temp = smbus2.i2c_msg.write(si7021_ADD,[si7021_READ_TEMPERATURE])

            #Set up a read transaction that reads two bytes of data
            read_result = smbus2.i2c_msg.read(si7021_ADD,2)

            #Execute the two transactions with a small delay between them
            inh.bus.i2c_rdwr(cmd_meas_temp)
            time.sleep(0.1)
            inh.bus.i2c_rdwr(read_result)
            print("OPENED threading lock")

        #convert the result to an int

        reading = int.from_bytes(read_result.buf[0]+read_result.buf[1],'big')

        if mode=="temp":
            value = self.conv_temperature(reading)
        else:
            value = self.conv_humidity(reading)

        print("Get reading temp_sensor ", value)

        return value


