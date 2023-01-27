import time
import smbus2
import json

def conv_temperature(value):
    """
    Converts the temperature value to relevant integer format

    """
    #temperature conv func
    temp = (175.72*value)/65536
    temp -= 6

    return temp

def make_array(temperature,curr_arr=[]):
    """This expands the created an array and writes to a file"""
    curr_arr.append(float(temperature))

    dict_values = {"temperatures":curr_arr}
    print("in make_array: ",dict_values)
    
    with open("temperature.json", "a") as out_file:
        json.dump(dict_values,out_file)
    out_file.close()
    time.sleep(0.5)
    
    return curr_arr




def read_temp():
    """
    
    Has an effect of reading temperature values from the sensor

    """
    diff_time = time.time()    
    si7021_ADD = 0x40 #Add the I2C bus address for the sensor here
    si7021_READ_TEMPERATURE = 0xE3 #Add the command to read temperature here

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
    temperature = int.from_bytes(read_result.buf[0]+read_result.buf[1],'big')
    print("displayin temperature", conv_temperature(temperature))
    return conv_temperature(temperature)

elapse_time = 0
curr_time = time.time()
arr_inspect = []


while elapse_time<8:

    #records for about 8 seconds and gets readings
    elapse_time= time.time()-curr_time
    get_temp = read_temp()
    arr_inspect = make_array(temperature=get_temp,curr_arr=arr_inspect)








