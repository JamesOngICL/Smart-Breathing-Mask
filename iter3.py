
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

URL = 'http://146.169.244.33:8080'



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
        """Reads the humidity byte value and converts to float."""

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

        bus = smbus2.SMBus(1)

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



print (" Reading Data of Gyroscope and Accelerometer")

#makes a queue where we can push data

'''To edit

def fifo_data_queue(make_q):
    curr_time = time.time()
    elapse_time = 0
    try:
        while elapse_time<15:
            elapse_time = time.time()-curr_time

            gen_random = random.randint(0,9)
            with open("debug.txt","a") as outp:
                outp.write(str(gen_random)+"\n")
            outp.close()
            time.sleep(0.4)

            make_q.put(gen_random)
    except KeyboardInterrupt:
        return
'''

def reading_to_queue(make_q):
    print("entered post thread")
    curr_time = time.time()
    elapse_time = 0
    try:
        print("Posting values")

        while True:
            # if KeyboardInterrupt:
            #     break

            elapse_time = time.time()-curr_time

            read_address = [0x3B,0x3D,0x3F]

            #deduce time elapsed
            init_acc = gyro_accelerometer_sensor()
            init_acc.initialize_accelerometer()
            #get accelerometer vectorized readings
            Ax, Ay, Az = init_acc.process_accelerometer_vals(read_address)
            postable_dict = {'Accelerometer':[Ax,Ay,Az]}

            #put data values in queue
            make_q.put(postable_dict)

            sleep(0.35)

            #get temperature readings vectorized
            init_temp = temp_hum_sensor()
            get_value = init_temp.read_temp_hum('temp')
            postable_dict = {'Temperature':get_value}

            #write data values in a queue.
            make_q.put(postable_dict)

            print(make_q)
            print("Temp:",get_value,"Ax:",Ax," Ay:",Ay)

            # outp.close()

            sleep(0.35)
    
    except KeyboardInterrupt:
        return
    
    pass


class post_to_server(threading.Thread):
    def __init__(self,name):
        threading.Thread.__init__(self)
        #characterizes the type of thread. Should this be
        self.name = name

    def run(self):
        #accesses the queues and puts data inside.
        print("Running a Post Thread - Takes Value from Queue")
        simulate_server(self.name)
        print("Thread is Terminating",self.name)
        pass



def simulate_server(thread_name):
    curr_time = time.time()

    elapse_time = 0
    print("before while true",thread_name)

    while True:
        elapse_time = time.time()-curr_time            
        
        # if KeyboardInterrupt:
        #         break

        try:
            print("in try loop")
            get_val = make_q.get(block=False)

        except queue.Empty:
            print("quEUE EMPTY")
            # if KeyboardInterrupt:
            #     break
            continue

        else:
            #posts this value to a JSON
            # if KeyboardInterrupt:
            #     break
            print("observe get_val",get_val)
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
            for key in get_val:
                tmp = get_val[key]
                if key=='Temperature':
                    put_key = 'Sensor:temperaturereading'
                else:
                    put_key = "Sensor:accelerometerreading"

            login_data = {'test':get_val, put_key:tmp,'address':'MS3120001','csrfmiddlewaretoken':csrftoken}
            
            print("Posting to Server:",login_data)

            r = client.post(URL, data=login_data, headers=dict(Referer=URL))
            time.sleep(0.001)
            track = track + 0.001
            print(len(r.text))

            # with open("my_test.json","a") as outp:
            #     json.dump(get_val,outp)
            #     json.dump("\\n\\",outp)
            # outp.close()

    return

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

