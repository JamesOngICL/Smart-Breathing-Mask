import smbus2					#import SMBus module of I2C
import time
import json

#relevant smbus params
gp_bus = smbus2.SMBus(3)

class measure_co2voc():
    
    '''
    
    A class to measure the volatile organic compounds and CO2 values that are present in the surrounding environment 

    '''

    def __init__(self,i2c_addr):
        
        '''

        Constructor to initalize the co2voc sensor and provide some variables that are easily accesible from all member functions. Function is of type void. 
        
        Inputs:
        type(hex) -> i2c_addr usually 0x5a. 

        '''
        self.addr = i2c_addr

        return 

    def init_co2_new(self):
        '''

        Function to initialize the carbon dioxide sensor to calibrate the sensor and allow this sensor to get readings from the surrounding atmosphere. 

        Inputs:
        type(self) -> corresponding to the class that was used. 

        Example usage:
        c1 = measure_vocs()
        c1.init_co2_new()

        '''


        #initalizes the smbus2 sensors mode
        stat_reg = 0x00
        addr = 0x5A
        app_reg = 0xF4
        reset_reg = 0xFF

        print("Running Initializations")

        #Resetthe CO2 sensor
        gp_bus.write_i2c_block_data(addr,reset_reg,[0x11,0xE5,0x72,0x8A])
        time.sleep(0.3)


        #write to the status register
        gp_bus.write_byte_data(addr,stat_reg,1)


        meas_mode = 0x01

        #Writing to application register
        gp_bus.write_i2c_block_data(addr,app_reg, [])
        time.sleep(0.3)
        
        # Set to 72 to increase sensor reading rate. See datasheet for justification. 
        gp_bus.write_byte_data(addr,meas_mode,24)

        # print("working")
        time.sleep(0.3)
        
        print("Finished CO2 Initialization")


    def read_vals(self):

        '''

        Function to read the Co2 sensor and volatile organic compound values from the Co2 sensors. 

        Inputs:
        type(self) -> corresponds to class with attributes
        
        Outputs:
        type(array) length 4 corresponding to the atmospheric CO2 level. 


        '''

        #reads the eco2 parameters and VOC level
        value_read = 0

        #set a time limit of 15 seconds for readings to be produced
        read_duration = 15
        curr_time = time.time()
        elapse_time = 0
        while elapse_time<read_duration:
            print("enter while loop")

            #deduce the current time passed see if data available. 

            elapse_time = time.time()-curr_time
            read_status = gp_bus.read_byte_data(self.addr,0x00)
            tmp = format(read_status,"#010b")[2:]
            time.sleep(0.5)

            #Control flow condition indicating that data is ready and avaialble
            if tmp[4]==str(1):
                top_eco2 = gp_bus.read_i2c_block_data(self.addr,0x02,8)
                time.sleep(0.1)
                return top_eco2

        return top_eco2

    def convert_vals(self,co2_air_qual):
            '''

            Processes the data returned by the read_vals function and will return the output Co2 levels and VOC levels

            Inputs:
            self - type(class) -> corresponding to class information
            co2_air_qual -> corresponds to sensor readings that were present on the co2 sensor.

            Outputs:
            type(array) [co2_level, voc_level] -> returns the calculated and processed co2 and volatile organic compound level. 
            
            '''
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

