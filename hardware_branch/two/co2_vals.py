import smbus2					#import SMBus module of I2C
from time import sleep          #import
import json
import time


import json

import time

import temperature as temp_sens
import threading_almost_fin as th

class measure_vocs():
    def __init__(self):

        return 

    def init_co2_new(self):


        #initalizes the smbus2 sensors mode
        stat_reg = 0x00
        addr = 0x5A
        app_reg = 0xF4
        reset_reg = 0xFF

        print("Running Initializations")

        #Resetthe CO2 sensor
        th.gp_bus.write_i2c_block_data(addr,reset_reg,[0x11,0xE5,0x72,0x8A])
        time.sleep(0.3)


        #write to the status register
        th.gp_bus.write_byte_data(addr,stat_reg,1)


        meas_mode = 0x01

        #Writing to application register
        th.gp_bus.write_i2c_block_data(addr,app_reg, [])
        time.sleep(0.3)

        # print(int(bin_a, 2)) #Base 2(binary)
        
        # Set to 72 to increase sensor reading rate. See datasheet for justification. 
        th.gp_bus.write_byte_data(addr,meas_mode,24)

        # print("working")
        time.sleep(0.3)
        
        print("Finished CO2 Initialization")


    def read_co2_vals(self,i2c_addr):

        #reads the eco2 parameters and VOC level
        value_read = 0
        # init_co2_new()


        #set a time limit of 15 seconds for readings to be produced
        read_duration = 15
        curr_time = time.time()
        elapse_time = 0
        while elapse_time<read_duration:
            print("enter while loop")

            #deduce the current time passed see if data available. 

            elapse_time = time.time()-curr_time
            read_status = th.gp_bus.read_byte_data(i2c_addr,0x00)
            tmp = format(read_status,"#010b")[2:]
            time.sleep(0.5)

            #Control flow condition indicating that data is ready and avaialble
            if tmp[4]==str(1):
                top_eco2 = th.gp_bus.read_i2c_block_data(i2c_addr,0x02,8)
                print("Reading CO2 levels",top_eco2)
                time.sleep(0.1)
                value_read = 1
                return top_eco2

        print("no data available")

        return top_eco2

    def convert_co2_vals(self,co2_air_qual):
            left_co2_val, right_co2_val = co2_air_qual[0],co2_air_qual[1]

            #gets the left_addr_val from CO2 sensor
            left_co2_val = left_co2_val<<8

            #aggregate the values to get co2_level
            co2_level = left_co2_val+right_co2_val

            #reads in a litle endian format.
            left_voc, right_voc = co2_air_qual[2], co2_air_qual[3]

            #gets the volatile organic copound level
            voc_level = (left_voc<<8)+right_voc

            #returns the co2 and volatile organic compounds levels
            return [co2_level,voc_level]

