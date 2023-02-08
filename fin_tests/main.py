
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

def reading_to_queue(make_q,lock):

    try:
        print("Posting values")

        #To tidy this while Loop looks very, very convoluted.
        while True:
            try:

                read_address = [0x3B,0x3D,0x3F]

                #get accelerometer vectorized readings
                print("init")
                init_acc = gyro_acc.gyro_accelerometer_sensor()
                print("init worked")
                init_acc.initialize_accelerometer()
                Ax, Ay, Az = init_acc.process_accelerometer_vals(read_address)
                postable_dict = {'Accelerometer':[Ax,Ay,Az]}

                #put data values in queue
                make_q.put(postable_dict)
                

                sleep(0.03)

                #get temperature readings vectorized
                init_temp = temp_sens.temp_hum_sensor()
                get_value = init_temp.read_temp_hum('temp')
                postable_dict = {'Temperature':get_value}
                make_q.put(postable_dict)

                #has the effect of putting locks that act as a thread safe data structure.
                # with lock:

                # with open("temp_acc.txt",'a') as file:

                #     my_str = "Temperature:"+str(get_value)+" ,Ax:"+str(Ax)+" ,Ay:"+str(Ay)," Az:"+str(Az)
                #     print(my_str)
                #     file.write(str(my_str)+"\n")

                # file.close()


                print("Temp:",get_value,"Ax:",Ax," Ay:",Ay)

                time.sleep(0.03)

            except KeyboardInterrupt:
                break

            except:
                print("Reached error in I2C")
                time.sleep(0.25)                
                
                # with open("readings.txt",'a') as file:
                #         my_str = "Temperature:"+str(init_temp)+" ,Ax:"+str(Ax)+" ,Ay:"+str(Ay)," Az:"+str(Az)
                #         print(my_str)
                #         file.write("ERRROR")
                # file.close()

    except KeyboardInterrupt:
        return




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

        else:

            # with open("my_test.json","w") as outp:
            #     #dump the q value to a json file
            #     json.dump(get_q_val,outp)

            #     #haha, this never actually wrote a new line it's a big fail.
            #     outp.write('\n')

            # outp.close()

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

            # reading_data = {'Sensor:temperaturereading':str(get_q_val),'address':'MS3120001'}
            MSG_INFO = client.publish("sensors/omar/readings", str(reading_data))
            print("Currently Sending:",reading_data)
            mqtt.error_string(MSG_INFO.rc)
            # print("Message Published: ", MSG_INFO.is_published())
        
        finally:
            with open("finally.txt",'w') as f_name:
                f_name.write("entered")
            f_name.close()
            time.sleep(0.03)
            continue



    return

def co2_to_queue(addr,make_q):

    co2_meas = co2_vals.measure_vocs()

    while True:

        try:
            
            temp_val = co2_meas.read_co2_vals(addr)
            conv_value = co2_meas.convert_co2_vals(temp_val)

            postable_dict = {'co2_air_qual':conv_value}
            make_q.put(postable_dict)

            print("converted CO2",conv_value)
            
            # with open("readings2.txt",'a') as file:
            #     my_str = "Co2 PPM: "+str(conv_value[0])+" ,VOC ppb: "+str(conv_value[1])
            #     file.write(str(my_str)+"\n")
                
            # file.close()

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

    m = heart.MAX30102()

    while True:
        try:
            #gets the heart rate and oxygen values and put them in a dictionary. 
            heart_rate_oxy = m.read_fifo()
            postable_dict = {'h_rate':m.read_fifo()}

            #push this to the global queue. 
            make_q.put(postable_dict)

            # with open("hr.txt",'w') as file:
            #     file.write("Heart_Rate: "+str(heart_rate_oxy))

            # file.close()


            # print("HR_OXY VALS",heart_rate_oxy)
            time.sleep(0.03)
        
        except KeyboardInterrupt:
            break
        
        except:
            print("need to initiate timeout")
            time.sleep(0.15)

def run_threads():
    #Run the Threads. 
    value_thread = threading.Thread(target=reading_to_queue,args=(make_q,lock),daemon=True)
    thread_co2 = threading.Thread(target=co2_to_queue,args=(0x5A,make_q),daemon=True)
    thread_heart_rate = threading.Thread(target=read_heart_rate, args=(make_q,),daemon=True)
    thread_post = post_to_server("my_test")
    
    print("---------Threads Initialized------------")   


    value_thread.start()
    thread_post.start()
    thread_co2.start()
    thread_heart_rate.start()

    pass

if __name__=="__main__":
    print("----Running the website----")
    run_threads()

