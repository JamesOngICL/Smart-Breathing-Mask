
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

'''

        init_dict = {"addr":[0x68],
        "reg":[0x19,0x6B,0x1A,0x38],"data":[7,1,0,1]}

        try:
            #initialize all four MPU6050 registers + addresses.
            for i in range(4):
                addr_key, reg, data = init_dict["addr"], init_dict["reg"],init_dict["data"]
                bus.write_byte_data(addr_key[0],reg[i],data[i])
'''

def init_co2_new():


    #initalizes the smbus2 sensors mode
    stat_reg = 0x00
    addr = 0x5A
    app_reg = 0xF4
    reset_reg = 0xFF

    print("Running Initializations")

    #Resetthe CO2 sensor
    bus.write_i2c_block_data(addr,reset_reg,[0x11,0xE5,0x72,0x8A])
    time.sleep(0.3)


    #write to the status register
    bus.write_byte_data(addr,stat_reg,1)


    meas_mode = 0x01

    #Writing to application register
    bus.write_i2c_block_data(addr,app_reg, [])
    time.sleep(0.3)

    # print(int(bin_a, 2)) #Base 2(binary)
    
    # Set to 72 to increase sensor reading rate. See datasheet for justification. 
    bus.write_byte_data(addr,meas_mode,24)

    # print("working")
    time.sleep(0.3)
    
    print("Finished CO2 Initialization")

    #App start



    #write to the error_id register
    # bus.write_byte_data(addr,error_id_reg,1)

def read_co2_vals(i2c_addr):

    #reads the eco2 parameters and VOC level
    value_read = 0

    #set a time limit of 12 seconds for readings to be produced
    read_duration = 12
    curr_time = time.time()
    elapse_time = 0

    while elapse_time<read_duration:

        #deduce the current time passed see if data available. 

        elapse_time = time.time()-curr_time
        read_status = bus.read_byte_data(i2c_addr,0x00)
        tmp = format(read_status,"#010b")[2:]
        time.sleep(0.5)

        #Control flow condition indicating that data is ready and avaialble
        if tmp[4]==str(1):
            top_eco2 = bus.read_i2c_block_data(i2c_addr,0x02,8)
            print("Reading CO2 levels",top_eco2)
            time.sleep(0.1)
            value_read = 1
            break

    print("no data available")

    return top_eco2

    # fml = bus.read_byte_data(0x5A,0x01)
    # # tmp = format(fml,"#010b")[2:]
    # tmp = bin(fml)
    # print("Reading meas_mode bit:",tmp,"FML val",fml)

    # pass
    # error_reg = 0xE0
    # temp2 = bus.read_byte_data(0x5A,0xE0)
    # print("Error Code is:",bin(temp2))
    # time.sleep(0.5)



init_co2_new()
curr_time = time.time()
elapse_time = 0

while elapse_time<45:
    print("TIME ELAPSED:",elapse_time)
    read_co2_vals(i2c_addr=0x5A)
    elapse_time = time.time()-curr_time








