
import smbus2					#import SMBus module of I2C
from time import sleep          #import
import json

import json

import time
import math
import RPi.GPIO as GPIO
import smbus
import threading



class heart_sensor():
    def __init__(self):
        '''
        
        Function that initializes all the relevant heart rate sensor values

        '''

        print("Initialized Heart Rate Sensor")
        self.address = 0x57 #address
        self.channel = 1 #channel
        self.bus = smbus.SMBus(1) #same as self.channel
        self.interrupt = 7 #gpio pin

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.interrupt, GPIO.IN)

        self.bus.write_i2c_block_data(self.address, 0x09, [0x40])

        sleep(1)

        reg_data = self.bus.read_i2c_block_data(self.address, 0x00, 1)

        with threading.Lock():
            #Initialize all the relevant I2C bus addresses. 
            self.bus.write_i2c_block_data(self.address, 0x02, [0xc0])
            self.bus.write_i2c_block_data(self.address, 0x03, [0x00])

            self.bus.write_i2c_block_data(self.address, 0x04, [0x00])
            self.bus.write_i2c_block_data(self.address, 0x05, [0x00])
            self.bus.write_i2c_block_data(self.address, 0x04, [0x00])

            self.bus.write_i2c_block_data(self.address, 0x08, [0x4f])
            self.bus.write_i2c_block_data(self.address, 0x09, [0x03])
            self.bus.write_i2c_block_data(self.address, 0x0A, [0x27])

            self.bus.write_i2c_block_data(self.address, 0x0C, [0x24])
            self.bus.write_i2c_block_data(self.address, 0x0D, [0x24])
            self.bus.write_i2c_block_data(self.address, 0x10, [0x7f])

    def set_config(self, reg, value):
        '''                
        Function that gets heart rate configurese writing to relevant i2c address and value sensor values

        Inputs:
        type(class)-> self, type(hex)-> reg, type(float)->value


        '''

        #write the i2c_block data needed for heart rate measurements. 
        self.bus.write_i2c_block_data(self.address, reg, value)

    def read_fifo(self):
        """

        This function will read the data register and return heart rate and oxygen saturation parameters. 

        Inputs:
        type(class)-> self. 

        Output:
        type(float)->red_led, type(float)->ir_led

        """
        red_led = None
        ir_led = None

        # read 1 byte from registers (values are discarded)
        with threading.Lock():
            reg_INTR1 = self.bus.read_i2c_block_data(self.address, 0x00, 1)
            reg_INTR2 = self.bus.read_i2c_block_data(self.address, 0x01, 1)

            # read 6-byte data from the device
            d = self.bus.read_i2c_block_data(self.address, 0x07, 6)

        # mask MSB [23:18]
        red_led = (d[0] << 16 | d[1] << 8 | d[2]) & 0x03FFFF
        ir_led = (d[3] << 16 | d[4] << 8 | d[5]) & 0x03FFFF

        return red_led, ir_led
