
import smbus2					#import SMBus module of I2C
from time import sleep          #import
import time

import json
import time
import random
# import threading_almost_fin as inh

import threading

bus = smbus2.SMBus(1) 	# or bus = smbus.SMBus(0) for older version boards


class gyro_accelerometer_sensor():

    def __init__(self):
        pass

    def initialize_accelerometer(self):
        """

        Initializes the accelerometer in python, possibly if the pins aren't in place this will break.

        Inputs:
        type(class) -> self. 

        """
        init_dict = {"addr":[0x68],
        "reg":[0x19,0x6B,0x1A,0x38],"data":[7,1,0,1]}

        try:
            #initialize all four MPU6050 registers + addresses.
            for i in range(4):
                addr_key, reg, data = init_dict["addr"], init_dict["reg"],init_dict["data"]
                with threading.Lock():
                    bus.write_byte_data(addr_key[0],reg[i],data[i])

        except:
            #error initializing addresses, useful unit test.
            return -1

        return 1

    def process_readings(self,first,second,threshold):

        """

        Helper function to map the relevant values from the accelerometer. Will be converted to OOP format

        """

        val = (first | second)

        #do mapping relative to threshold values.
        if (val > threshold):
            return (val-65536)

        return val

    def read_raw_data(self,addr):

            """

            Extracts the relevant data from the accelerometer and gyroscope sensor.

            Inputs:
            type(class)->self, type(hex)->addr

            Output:
            get_val -> represented as bytes

            """
            #get the top address and do bitwise shifting
            top = (bus.read_byte_data(0x68, addr))<<8

            #pause to avoid race conditions
            time.sleep(0.1)

            #get bottom value
            bot = bus.read_byte_data(0x68, addr+1)

            #get values.
            get_val = self.process_readings(first=top,second=bot,threshold=32678)

            return get_val

    def process_accelerometer_vals(self,inp_addr):
        """

        Function to process the input accelerometer values present from the input address

        Inputs:
        type(self), type(hex)->inp_addr

        Output:
        type(float), type(float), type(float) -> representing the g value accelerometer value. 

        """
        x_inp = self.read_raw_data(inp_addr[0])
        y_inp = self.read_raw_data(inp_addr[1])
        z_inp = self.read_raw_data(inp_addr[2])

        map_vals = lambda val : val/16384.0

        return map_vals(x_inp),map_vals(y_inp),map_vals(z_inp)

