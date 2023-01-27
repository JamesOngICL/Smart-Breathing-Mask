import time
import smbus2

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
print(temperature)
