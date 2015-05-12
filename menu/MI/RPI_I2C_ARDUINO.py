# Communication between RPI and Arduino, using I2C
# Goal: 
#	RPI should be able to recieve data from Arduino, and send data to Arduino to adjust
# 	some parameters. The reason of using I2C instead of other method:
# 	1. serial port monitor is 
# 	not be able to implement our GUI.
# 	2. Serial communication ports are taken up for Arduino 
# 	communication with the furnace built-in temperature controller

import smbus
import time

bus = smbus.SMBus(1)    # 0 = /dev/i2c-0 (port I2C0), 1 = /dev/i2c-1 (port I2C1)

addr = 0x04      #7 bit address (will be left shifted to add the read write bit)
some_reg = input("Please enter fucntion code: ")
data = input("Please enter value: ")

some_reg1 = some_reg
data1 = data

def StringToBytes(data):
	retVal = []
	for c in data:
		retVal.append(ord(c))
	return retVal

def getStatus(addr):
        status = ""
        for i in range (0, 30):
            status += chr(bus.read_byte(addr))
        #    time.sleep(0.05);
        #time.sleep(0.01)        
        return status


data = StringToBytes(data)
some_reg = ord(some_reg[0].upper())


bus.write_i2c_block_data(addr, some_reg, data)
time.sleep(0.1)

status = getStatus(addr)


#bus.read_byte(addr)

#print "Arduino: Hey RPI, I received a digit ", some_reg1 + data1
print "Arduino1: Hey RPI, I received a word: ", status

	









