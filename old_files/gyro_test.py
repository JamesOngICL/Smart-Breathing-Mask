import smbus2					#import SMBus module of I2C
from time import sleep          #import
import json
import time

#some MPU6050 Registers and their Address


def conv_temperature(value):
    """
    Converts the temperature value to relevant integer format

    """
    #temperature conv func
    temp = (175.72*value)/65536
    temp -= 46.85

    return temp

def conv_humidity(value):
    """Reads the humidity byte value and converts to float."""

    #humidity mapping function
    humidity = 125*value/65536
    humidity -= 6

    return humidity

def make_array(temperature,curr_arr=[]):

    """This expands the created an array and writes to a file"""

    curr_arr.append(float(temperature))

    dict_values = {"temperatures":curr_arr}
    print("in make_array: ",dict_values)

    with open("temperature.json", "w") as out_file:
        json.dump(dict_values,out_file)
    out_file.close()
    time.sleep(0.5)

    return curr_arr


def read_temp_hum(mode):
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
        value = conv_temperature(reading)
    else:
        value = conv_humidity(reading)

    print("Get reading temp_sensor ", value)

    return value



def initialize_accelerometer():
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

def process_readings(first,second,threshold):

    """

    Helper function to map the relevant values from the accelerometer. Will be converted to OOP format

    """

    val = (first | second)

    #do mapping relative to threshold values.
    if (val > threshold):
        return (val-65536)

    return val





def read_raw_data(addr):

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
        get_val = process_readings(first=top,second=bot,threshold=32678)

        return get_val

def process_accelerometer_vals(inp_addr):
    """

    Function to process the input accelerometer values present from the input address

    """
    x_inp = read_raw_data(inp_addr[0])
    y_inp = read_raw_data(inp_addr[1])
    z_inp = read_raw_data(inp_addr[2])

    map_vals = lambda val : val/16384.0

    return map_vals(x_inp),map_vals(y_inp),map_vals(z_inp)


bus = smbus2.SMBus(1) 	# or bus = smbus.SMBus(0) for older version boards
#Device_Address = 0x68   # MPU6050 device address

initialize_accelerometer()

print (" Reading Data of Gyroscope and Accelerometer")

elapse_time = 0
curr_time = time.time()
arr_inspect = []


while elapse_time<50:

	#Read Accelerometer raw value
	read_address = [0x3B,0x3D,0x3F]

	#deduce time elapsed
	elapse_time = time.time()-curr_time

	#get accelerometer vectorized readings
	Ax, Ay, Az = process_accelerometer_vals(read_address)

	print ("\tAx=%.2f g" %Ax, "\tAy=%.2f g" %Ay, "\tAz=%.2f g" %Az)
	sleep(0.85)

	#get temperature readings vectorized
	get_value = read_temp_hum('temp')
	print("Read Temperature As: ",get_value)
	sleep(0.85)
