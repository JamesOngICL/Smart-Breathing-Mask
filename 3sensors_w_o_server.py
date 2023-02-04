
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


def reading_to_queue(make_q):

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

            sleep(0.05)

            #get temperature readings vectorized
            init_temp = temp_hum_sensor()
            get_value = init_temp.read_temp_hum('temp')
            postable_dict = {'Temperature':get_value}
            make_q.put(postable_dict)

            with open("readings.txt",'a') as file:
                file.write("Temperature:",str(init_temp)," ,Ax:",str(Ax)," ,Ay:",str(Ay)," Az:",str(Az))
            file.close()

            print("Temp:",get_value,"Ax:",Ax," Ay:",Ay)

            sleep(0.05)

            air_reader = air_sensor(0x5A)

            #setup the first time. 
            air_reader.setup_co2_sensor()
            air_reader.get_air_params()
            air_readings = air_reader.get_co2_vol_comp()
            postable_dict = {'co2_air_qual':air_readings}
            make_q.put(postable_dict)

            with open("readings.txt",'a') as file:
                file.write("Co2 PPM:",str(air_readings[0])," ,VOC ppb:",str(air_readings[1]))
            file.close()



            
            sleep(0.05)



    
    except KeyboardInterrupt:
        return
    
    pass


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
        post_to_server(self.name)
        print("Thread is Terminating",self.name)

        pass



def post_to_server(thread_name):

    '''
    
    A function that runs a thread to post data to server. Access data from a global queue that is shared amongst threads and then will post the data to a server. Multithreading necessary especially because of CO2 sensor. Want some data to be processable from sensors without having to wait for all readings to be taken.


    Variables:
    (Input) -> thread_name just exists pertaining to the class thread name
    (Global Queue) -> make_q is a global queue which operates as a thread safe data structure.
    (Functionality) -> Posts data to server like a void type in C++ arduino
    
    '''

    curr_time = time.time()

    elapse_time = 0
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
                json.dump("\\n\\",outp)
            
            outp.close()

    return

'''

Handles posting to HTTP may be legacy code

print("observe get_val",get_q_val)
track = 0
client = requests.session()
# Retrieve the CSRF token first
client.get(URL)  # sets cookie
if 'csrftoken' in client.cookies:
    # Django 1.6 and up
    csrftoken = client.cookies['csrftoken']
else:
    # older versions
    csrftoken = client.cookies['csrf']

y = 40*math.sin((track/10)*32*3.14)+50
put_key = ""
for key in get_q_val:
    tmp = get_q_val[key]
    if key=='Temperature':
        put_key = 'Sensor:temperaturereading'
    else:
        put_key = "Sensor:accelerometerreading"

login_data = {'test':get_q_val, put_key:tmp,'address':'MS3120001','csrfmiddlewaretoken':csrftoken}

print("Posting to Server:",login_data)

r = client.post(URL, data=login_data, headers=dict(Referer=URL))
time.sleep(0.001)
track = track + 0.001
print(len(r.text))

'''


elapse_time = 0
curr_time = time.time()
arr_inspect = []



make_q = queue.Queue()

value_thread = threading.Thread(target=reading_to_queue,args=(make_q,),daemon=True)

thread_post = post_to_server("my_test")
value_thread.start()
thread_post.start()

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

