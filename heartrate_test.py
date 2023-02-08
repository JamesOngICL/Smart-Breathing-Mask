from __future__ import print_function
from time import sleep

import RPi.GPIO as GPIO
import smbus

class MAX30102():
    def __init__(self):
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
        self.bus.write_i2c_block_data(self.address, reg, value)

    def read_fifo(self):
        """
        This function will read the data register.
        """
        red_led = None
        ir_led = None

        # read 1 byte from registers (values are discarded)
        reg_INTR1 = self.bus.read_i2c_block_data(self.address, 0x00, 1)
        reg_INTR2 = self.bus.read_i2c_block_data(self.address, 0x01, 1)

        # read 6-byte data from the device
        d = self.bus.read_i2c_block_data(self.address, 0x07, 6)

        # mask MSB [23:18]
        red_led = (d[0] << 16 | d[1] << 8 | d[2]) & 0x03FFFF
        ir_led = (d[3] << 16 | d[4] << 8 | d[5]) & 0x03FFFF

        return red_led, ir_led

m = MAX30102()
for i in range(100000):
    print(m.read_fifo()[1])
