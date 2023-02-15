
import smbus2					
from time import sleep          
import json
import time

import queue
import threading
import json
import time
import RPi.GPIO as GPIO
import smbus
import random
import rsa
import binascii

import temperature as temp_sens
import gyro_acc, co2_vals, heart
import paho.mqtt.client as mqtt 


bus = smbus2.SMBus(1) 	# or bus = smbus.SMBus(0) for older version boards

#Device_Address = 0x68   # MPU6050 device address
gp_bus = smbus2.SMBus(3)

# Initialize a queue data structure for thread safety.
make_q = queue.Queue()

#Lock if thread cannnot be 
lock = threading.Lock()


class post_to_server(threading.Thread):
    def __init__(self,name):
        '''

        How multiple threads are handled in python. See documentation for python multithreading protocols.

        '''
        threading.Thread.__init__(self)
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

        except:
            time.sleep(0.05)

        else:

            client = mqtt.Client('raspberry_pi_test')
            client.connect("146.169.253.62",port=1883)
            
            if 'Temperature' in get_q_val:
                # print("preposting",get_q_val['Temperature'])
                reading_data = {'Sensor:temperaturereading':str(round(get_q_val['Temperature'], 3)),'address':'MS3120001'}
            elif 'Accelerometer' in get_q_val:
                # print(get_q_val['Accelerometer'])
                new_data = [(get_q_val['Accelerometer'][0]), (get_q_val['Accelerometer'][1]), (get_q_val['Accelerometer'][2])]
                reading_data = {'Sensor:accelerometerreading': str(new_data),'address':'MS3120001'}
                
            elif 'h_rate' in get_q_val:
                reading_data = {'Sensor:heartratereading':str(get_q_val['h_rate'][0]),'address':'MS3120001'}

            elif 'co2_air_qual' in get_q_val:
                new_data = [(get_q_val['co2_air_qual'][0]), (get_q_val['co2_air_qual'][1])]
                reading_data = {'Sensor:co2reading':str(new_data),'address':'MS3120001'}
            else:
                continue

            MSG_INFO = client.publish("sensors/omar/readings", encrypt(str(reading_data),key))
            print("Currently Sending:",reading_data)
            mqtt.error_string(MSG_INFO.rc)
            time.sleep(0.01)
            # print("Message Published: ", MSG_INFO.is_published())


    return

def getkey():
    '''
    Function that will generate a public key necessary for posting to MQTT.
    '''
    public_key = rsa.PublicKey(17822536325291103101323819498187309223540366914795284790480275832907387155167793075777561150522889142593001669196266128814411559496746832319118549807122213726549864914547111915612810151458421841885576703978191424830064979840625261982526983948534265579315189645712708057829444744526097651478257973249834256433525747544157305555064689911278584472322809386995238704397789909958860784202773540915843232935732240372781175094908655965143500697948600899964661078620371137797175431929993230441845012688184755850715508366128027618816784376158765529688868977572400965001046656964586523083679277864216337830024186581266532501199, 65537)
    return public_key

def encrypt(message,key):
    """"
    Protocol to encrypt the relevant message information and the information can be sent to the server. 
    """
    return binascii.hexlify(rsa.encrypt(message.encode(),key)).decode()

#gets the public postable key. 
key = getkey()



def process_vals(mode):
    '''
    Helper function to process temperature and acceleration values. 
    
    Input: mode -> temp, acc. 

    '''

    #get accelerometer vectorized readings
    if mode =="temp":
        #inits sensor
        init_temp = temp_sens.temp_hum_sensor()
        
        #gets temperature readings after initializing sensor
        get_temp = init_temp.read_temp_hum('temp')

        return get_temp

    
    elif mode=="acc":
        read_address = [0x3B,0x3D,0x3F]
        init_acc = gyro_acc.gyro_accelerometer_sensor()
        init_acc.initialize_accelerometer()
        Ax, Ay, Az = init_acc.process_accelerometer_vals(read_address)
        return Ax,Ay,Az


def get_temp_acc(make_q,lock):
    
    '''
    
    Runs a function to get and extract the raw temperature and acceleration values and place 
    them within a queue data structure. 
    
    '''

    try:
        print("Posting values")

        while True:
            try:
                #get value for acceleration
                Ax,Ay,Az = process_vals("acc")
                postable_dict = {'Accelerometer':[Ax,Ay,Az]}
                
                #put data values in queue
                make_q.put(postable_dict)
                

                sleep(0.018)

                #get temperature readings vectorized
                get_temp = process_vals("temp")
                postable_dict = {'Temperature':get_temp}
                make_q.put(postable_dict)

                print("Temp:",get_temp,"Ax:",Ax," Ay:",Ay)

                sleep(0.018)

            except KeyboardInterrupt:
                break

            except:
                print("Reached error in I2C")
                gen_rand = (random.randint(5,45))/100
                time.sleep(gen_rand)                
                

    except KeyboardInterrupt:
        return





def co2_to_queue(addr,make_q):
    '''
    
    Calls the CO2 class in a thread initalized later and will send data to the shared queue resource.  
    
    '''

    co2_meas = co2_vals.measure_vocs()

    while True:

        try:
            
            temp_val = co2_meas.read_co2_vals(addr)
            conv_value = co2_meas.convert_co2_vals(temp_val)

            postable_dict = {'co2_air_qual':conv_value}
            make_q.put(postable_dict)

            print("converted CO2",conv_value)
            

        except KeyboardInterrupt:
            break

        except:
            co2_meas.init_co2_new()
            time.sleep(0.2)

    pass

def read_heart_rate(make_q):
    '''

    Function to read the CO2 sensors including initializations 

    '''

    m = heart.heart_sensor()

    while True:
        try:
            #gets the heart rate and oxygen values and put them in a dictionary. 
            heart_rate_oxy = m.read_fifo()
            postable_dict = {'h_rate':m.read_fifo()}

            #push this to the global queue. 
            make_q.put(postable_dict)

            time.sleep(0.03)
        
        except KeyboardInterrupt:
            break
        
        except:
            print("need to initiate timeout due to I2C error")
            new_rand = (random.randint(6,60))/100
            time.sleep(new_rand)

def run_threads():
    '''
    
    Calling this function will result in all 4 threads being triggered and running on the main thread. 
    
    ''' 
    
    #Name and intialize the threads
    value_thread = threading.Thread(target=get_temp_acc,args=(make_q,lock),daemon=True)
    thread_co2 = threading.Thread(target=co2_to_queue,args=(0x5A,make_q),daemon=True)
    thread_heart_rate = threading.Thread(target=read_heart_rate, args=(make_q,),daemon=True)
    thread_post = post_to_server("Server_Thread")
    
    print("---------Threads Initialized------------")   

    #Runs the relevant threads
    value_thread.start()
    thread_post.start()
    thread_co2.start()
    thread_heart_rate.start()

    pass

if __name__=="__main__":
    print("----Running the website----")
    run_threads()

