
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

from adafruit_extended_bus import ExtendedI2C as I2C


URL = 'http://146.169.252.125:8080'



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

    def make_array(self,temperature,curr_arr=[]):

        """This expands the created an array and writes to a file"""

        curr_arr.append(float(temperature))

        dict_values = {"temperatures":curr_arr}
        print("in make_array: ",dict_values)

        with open("temperature.json", "w") as out_file:
            json.dump(dict_values,out_file)
        out_file.close()
        time.sleep(0.5)

        return curr_arr


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
        cmd_meas_temp = smbus2.i2c_msg.write(si7021_ADD,[si7021_READ_TEMPERATURE])

        #Set up a read transaction that reads two bytes of data
        read_result = smbus2.i2c_msg.read(si7021_ADD,2)

        #Execute the two transactions with a small delay between them
        bus.i2c_rdwr(cmd_meas_temp)
        time.sleep(0.1)
        bus.i2c_rdwr(read_result)

        #convert the result to an int

        reading = int.from_bytes(read_result.buf[0]+read_result.buf[1],'big')

        if mode=="temp":
            value = self.conv_temperature(reading)
        else:
            value = self.conv_humidity(reading)

        print("Get reading temp_sensor ", value)

        return value


class gyro_accelerometer_sensor():

    def __init__(self):
        pass

    def initialize_accelerometer(self):
        """

        Initializes the accelerometer in python, possibly if the pins aren't in place this will break.

        """
        init_dict = {"addr":[0x68],
        "reg":[0x19,0x6B,0x1A,0x38],"data":[7,1,0,1]}

        try:
            #initialize all four MPU6050 registers + addresses.
            for i in range(4):
                addr_key, reg, data = init_dict["addr"], init_dict["reg"],init_dict["data"]
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

            """
            #get the top address and do bitwise shifting
            top = (bus.read_byte_data(0x68, addr))<<8

            #pause to avoid race conditions
            sleep(0.1)

            #get bottom value
            bot = bus.read_byte_data(0x68, addr+1)

            #get values.
            get_val = self.process_readings(first=top,second=bot,threshold=32678)

            return get_val

    def process_accelerometer_vals(self,inp_addr):
        """

        Function to process the input accelerometer values present from the input address

        """
        x_inp = self.read_raw_data(inp_addr[0])
        y_inp = self.read_raw_data(inp_addr[1])
        z_inp = self.read_raw_data(inp_addr[2])

        map_vals = lambda val : val/16384.0

        return map_vals(x_inp),map_vals(y_inp),map_vals(z_inp)


bus = smbus2.SMBus(1) 	# or bus = smbus.SMBus(0) for older version boards
gp_bus = smbus2.SMBus(3)
#Device_Address = 0x68   # MPU6050 device address


print (" Reading Data of Files")



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
        gp_bus.write_i2c_block_data(self.addr,self.reset_reg,[0x11,0xE5,0x72,0x8A])
        time.sleep(0.3)

        #write to the status register
        gp_bus.write_byte_data(self.addr,self.stat_reg,1)

        #Writing to application register
        gp_bus.write_i2c_block_data(self.addr,self.app_reg, [])
        time.sleep(0.3)

        # Set to 72 to increase sensor reading rate. See datasheet for justification.
        gp_bus.write_byte_data(self.addr,self.meas_mode,24)

        # print("working")
        time.sleep(0.3)
        print("Finished CO2 Initialization")

        return



    def get_air_params(self):

        '''

        Function to update the self.co2_air_qual parameter

        '''

        #set a time limit of 12 seconds for readings to be produced
        read_duration = 14
        curr_time = time.time()
        elapse_time = 0

        while elapse_time<read_duration:

            #deduce the current time passed see if data available.
            elapse_time = time.time()-curr_time
            # print("Oggles")

            read_status = gp_bus.read_byte_data(self.addr,0x00)
            # print("read_status",read_status)

            tmp = format(read_status,"#010b")[2:]
            time.sleep(0.5)
            co2_air_qual = gp_bus.read_i2c_block_data(self.addr,0x02,4)
            # print("debug ",co2_air_qual)
            print("oops",co2_air_qual,tmp)

            #Control flow condition indicating that data is ready and avaialble
            if tmp[4]==str(1):
                print("entering the condition")

                co2_air_qual = gp_bus.read_i2c_block_data(self.addr,0x02,4)
                # print("Reading CO2 & Air Quality Levels",co2_air_qual)

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
        #Try to process co2 data and send this. Error handling in class rather than multithread.
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
            #error handling function
            return None


#makes a queue where we can push data



def reading_to_queue(make_q,lock):

    print("entered post thread")
    curr_time = time.time()
    elapse_time = 0

    try:
        print("Posting values")

        #To tidy this while Loop looks very, very convoluted.
        while True:

            elapse_time = time.time()-curr_time

            read_address = [0x3B,0x3D,0x3F]

            #get accelerometer vectorized readings
            init_acc = gyro_accelerometer_sensor()
            init_acc.initialize_accelerometer()
            Ax, Ay, Az = init_acc.process_accelerometer_vals(read_address)
            postable_dict = {'Accelerometer':[Ax,Ay,Az]}

            #put data values in queue
            make_q.put(postable_dict)

            sleep(0.25)

            #get temperature readings vectorized
            init_temp = temp_hum_sensor()
            get_value = init_temp.read_temp_hum('temp')
            postable_dict = {'Temperature':get_value}
            make_q.put(postable_dict)

            #has the effect of putting locks that act as a thread safe data structure.
            with lock:

                with open("readings.txt",'a') as file:
                    my_str = "Temperature:"+str(init_temp)+" ,Ax:"+str(Ax)+" ,Ay:"+str(Ay)," Az:"+str(Az)
                    print(my_str)
                    file.write(str(my_str)+"\n")
                file.close()


            print("Temp:",get_value,"Ax:",Ax," Ay:",Ay)

            sleep(0.25)


    except KeyboardInterrupt:
        return




class post_to_server(threading.Thread):
    def __init__(self,name):
        '''

        How multiple threads are handled in python. See documentation for python multithreading protocols.

        '''

        #just initializes the thread it's nice.
        threading.Thread.__init__(self)

        #characterizes the name of the thread. Should this be
        self.name = name

    def run(self):

        '''

        API to allow the post_to_server thread to work and operate. This is a default class method in the threading class.

        '''

        #accesses the queues and puts data inside.
        print("Running a Post Thread - Takes Value from Queue")
        thread_to_server(self.name)
        print("Thread is Terminating",self.name)

        pass



def thread_to_server(thread_name):

    '''

    A function that runs a thread to post data to server. Access data from a global queue that is shared amongst threads and then will post the data to a server. Multithreading necessary especially because of CO2 sensor. Want some data to be processable from sensors without having to wait for all readings to be taken.


    Variables:
    (Input) -> thread_name just exists pertaining to the class thread name
    (Global Queue) -> make_q is a global queue which operates as a thread safe data structure.
    (Functionality) -> Posts data to server like a void type in C++ arduino

    '''

    print("before while true",thread_name)

    #
    while True:

        try:
            #attempt to extract data from the queue.
            get_q_val = make_q.get(block=False)

        except queue.Empty:

            continue

        else:

            with open("my_test.json","a") as outp:
                #dump the q value to a json file
                json.dump(get_q_val,outp)

                #haha, this never actually wrote a new line it's a big fail.
                outp.write('\n')

            outp.close()

    return

'''
def co2_posting(lock):



    #setup the first time.

    while True:
        try:
            #Initialize the air sensor
            air_reader = air_sensor(0x5A)
            #Gets the readings of CO2 etc from the sensor
            print("Attempting to get readings")
            air_reader.setup_co2_sensor()
            air_reader.get_air_params()
            air_readings = air_reader.get_co2_vol_comp()


            #Puts values into the postable dictionary
            postable_dict = {'co2_air_qual':air_readings}
            make_q.put(postable_dict)

            #Open a relevant threading lock
            print("Using a multithreaded lock",postable_dict)
            # lock.acquire()

            with open("readings2.txt",'a') as file:
                my_str = "Co2 PPM: "+str(air_readings[0])+" ,VOC ppb: "+str(air_readings[1])
                file.write(str(my_str)+"\n")
            file.close()

            #Close the threading lock
            # lock.release()

            #Get sensor to sleep.
            sleep(0.25)

        except KeyboardInterrupt:
            print("Keyboard Interrupt")
            break

        except:
            print("entered error, but I think it's fine")
            time.sleep(0.2)

    return postable_dict


class read_slow_sensor(threading.Thread):
    def __init__(self,name,args=()):
        #aimed primarily at reading the slow Co2 sensor

        #Start a CO2 thread
        threading.Thread.__init__(self)

        #Name this thread
        self.name = name
        self.lock = "Trying"

        #put thread arguments as args


    def run(self):
        

        This is an API allowing the thread to read a slow sensor from the GPIO bus scheduler. Not sure if the software I2C will have bugs but can try.

        

        print("running co2 API")

        #Posts the CO2 data with the API.
        co2_posting(self.lock)

        print("Finishing")
        pass
'''
gp_bus = smbus2.SMBus(3)

'''

        init_dict = {"addr":[0x68],
        "reg":[0x19,0x6B,0x1A,0x38],"data":[7,1,0,1]}

        try:
            #initialize all four MPU6050 registers + addresses.
            for i in range(4):
                addr_key, reg, data = init_dict["addr"], init_dict["reg"],init_dict["data"]
                bus.write_byte_data(addr_key[0],reg[i],data[i])
'''


    #App start



    #write to the error_id register
    # bus.write_byte_data(addr,error_id_reg,1)

'''

        try:
            #Initialize the air sensor
            air_reader = air_sensor(0x5A)
            #Gets the readings of CO2 etc from the sensor
            print("Attempting to get readings")
            air_reader.setup_co2_sensor()
            air_reader.get_air_params()
            air_readings = air_reader.get_co2_vol_comp()


            #Puts values into the postable dictionary
            postable_dict = {'co2_air_qual':air_readings}
            make_q.put(postable_dict)

            #Open a relevant threading lock
            print("Using a multithreaded lock",postable_dict)
            # lock.acquire()

            with open("readings2.txt",'a') as file:
                my_str = "Co2 PPM: "+str(air_readings[0])+" ,VOC ppb: "+str(air_readings[1])
                file.write(str(my_str)+"\n")
            file.close()

            #Close the threading lock
            # lock.release()

            #Get sensor to sleep.
            sleep(0.25)

        except KeyboardInterrupt:
            print("Keyboard Interrupt")
            break

        except:
            print("entered error, but I think it's fine")
            time.sleep(0.2)
'''


def oops_new(addr):
    co2_meas = measure_vocs()
    while True:
        try:
            
            temp_val = co2_meas.read_co2_vals(addr)
            conv_value = co2_meas.convert_co2_vals(temp_val)


            postable_dict = {'co2_air_qual':conv_value}
            make_q.put(postable_dict)

            print("converted CO2",conv_value)
            
            with open("readings2.txt",'a') as file:
                my_str = "Co2 PPM: "+str(conv_value[0])+" ,VOC ppb: "+str(conv_value[1])
                file.write(str(my_str)+"\n")
            file.close()

        except KeyboardInterrupt:
            break

        except:
            co2_meas.init_co2_new()
            time.sleep(0.2)

    pass

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
        gp_bus.write_i2c_block_data(addr,reset_reg,[0x11,0xE5,0x72,0x8A])
        time.sleep(0.3)


        #write to the status register
        gp_bus.write_byte_data(addr,stat_reg,1)


        meas_mode = 0x01

        #Writing to application register
        gp_bus.write_i2c_block_data(addr,app_reg, [])
        time.sleep(0.3)

        # print(int(bin_a, 2)) #Base 2(binary)
        
        # Set to 72 to increase sensor reading rate. See datasheet for justification. 
        gp_bus.write_byte_data(addr,meas_mode,24)

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
            read_status = gp_bus.read_byte_data(i2c_addr,0x00)
            tmp = format(read_status,"#010b")[2:]
            time.sleep(0.5)

            #Control flow condition indicating that data is ready and avaialble
            if tmp[4]==str(1):
                top_eco2 = gp_bus.read_i2c_block_data(i2c_addr,0x02,8)
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



elapse_time = 0
curr_time = time.time()
arr_inspect = []



make_q = queue.Queue()

lock = threading.Lock()


#Simulate the CO2 and temperature sensors.
# value_thread = threading.Thread(target=reading_to_queue,args=(make_q,lock),daemon=True)
thread_co2 = threading.Thread(target=oops_new,args=(0x5A,),daemon=True)

#Simulate the server by posting
thread_post = post_to_server("my_test")

#Simulate the GPIO CO2 sensor posting.
# thread_co2 = read_slow_sensor("test_CO2")


# value_thread.start()
thread_post.start()
thread_co2.start()

print("---------Threads Initialized------------")
curr_time = time.time()

elapse_time = 0
print("first elapse",elapse_time)

'''
while True:
    if KeyboardInterrupt:
        break
    elapse_time = time.time()-curr_time
'''

# value_thread.join()
# thread_post.join()

# while elapse_time<15:

# 	#Read Accelerometer raw value
#     read_address = [0x3B,0x3D,0x3F]

#     #deduce time elapsed
#     elapse_time = time.time()-curr_time
#     reading_to_queue(make_q)


'''





#puts value into the multithreaded target

'''

