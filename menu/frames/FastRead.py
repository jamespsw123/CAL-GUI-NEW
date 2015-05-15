# fast reading data
import spidev
import time
import os
# Open SPI bus
spi = spidev.SpiDev()
spi.open(0,0)
# Define sensor channel
ADT = 0
Vref = 3.3
#TMP36 = 1

# Function to read SPI data from MCP3008 chip
def ReadChannel_10bit(channel):
	# When using MCP3008(10 bit adc)
	adc = spi.xfer2([1,(8+channel)<<4,0])
	data = ((adc[1]&3) << 8) + adc[2]
	return data

def ReadChannel_12bit(channel):
	adc = spi.xfer2([(6 + (channel >> 2)), ((channel &3) << 6), 0])
	data = ((adc[1]&15 << 8) + (adc[2]))
	return data

# Function to convert data to voltage level,
# Rounded to specified number of decimal places.
def ConvertVolts_10bit(data, places):
	# When using MCP3008(10 bit adc)
	volts = (data*Vref)/float(1023)
	volts = round(volts, places)
	return volts

def ConvertVolts_12bit(data, places):
	# When using MCP3208(12 bit adc)
	volts = (data*Vref)/float(4095)
	volts = round(volts, places)
	return volts


# Function to calculate temperature from TMP36
# Rounded to specified number of decimal places.
"""
def ConvertTemp_TMP36(data, places):

	temp = ((data*330)/float(1023))-45
	temp = round(temp, places)
	return temp
"""

# Define delay between readings
#delay = 0.00001
# Define the length of the test
#length = 10.0
# Create two lists to store the temperature data and corresponding time
#i = 0
def fastRead(frequency, temp):
	delay = 1.0/frequency
	# Create two lists to store the temperature data and corresponding time
	"""
	# If we are using IR SENSOR PSC-T42L, whose measurement
	# range is -40C to 1000C. Its output current is 4 to 20mA, 
	# by mapping temp to current we get their relationship:
	current  = ((1.0/65.0)*temp + (60.0/13.0))/1000.0
	# when using 3.3v Vref, load resister = 3.3/0.02 = 165
	target_volt = 165*(current)
	"""
	# We are using IR Sensor Sirius SI23, whose measurement
	# range is 150C to 900C. Its output current is 4 to 20mA,
	# mapping temp to current, we get their relationship:
	current = ((8.0/375)*temp + (0.8))/1000.0 
	# when using 3.3v Vref, load resister = 3.3/0.02 = 165
	target_volt = 165.0*(current)
	# when using MCP3008(10 bit adc)
	#threshold = (target_volt*1023)/3.3

	# when using MCP3208(12 bit adc)
	threshold = (target_volt*4095)/3.3
	temp_level=[]
	time_elapsed = []
	StartTime = time.time()
	while (ReadChannel(ADT) > threshold):
		# read from sensor	
		temp_level.append(ReadChannel_12bit(ADT))
		time_elapsed.append(time.time() - StartTime)
		time.sleep(delay)

	#spi.close()
	# print "Delay Time = %r"%delay
	# print "Actual sample points recored in 10 seconds: %r"%(len(temp_level))
	return time_elapsed,temp_level
	




