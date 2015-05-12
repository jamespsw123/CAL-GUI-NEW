# fast reading data
import spidev
import time
import os
# Open SPI bus
spi = spidev.SpiDev()
spi.open(0,0)
# Define sensor channel
ADT = 0
TMP36 = 1

# Function to read SPI data from MCP3008 chip
def ReadChannel(channel):
	adc = spi.xfer2([1,(8+channel)<<4,0])
	data = ((adc[1]&3) << 8) + adc[2]
	return data

# Function to convert data to voltage level,
# Rounded to specified number of decimal places.
def ConvertVolts(data, places):
	volts = (data*3.3)/float(1023)
	volts = round(volts, places)
	return volts

# Function to calculate temperature from TMP36
# Rounded to specified number of decimal places.
def ConvertTemp_TMP36(data, places):

	temp = ((data*330)/float(1023))-45
	temp = round(temp, places)
	return temp

# Define delay between readings
#delay = 0.00001
# Define the length of the test
#length = 10.0
# Create two lists to store the temperature data and corresponding time
#i = 0
def CoolingProcess(delay, length):
	# Create two lists to store the temperature data and corresponding time
	temp_level=[]
	time_elapsed = []
	StartTime = time.time()
	while (time.time() - StartTime <= length):
		# Read the TMP36 sensor data	

		temp_level.append(ReadChannel(ADT))
		time_elapsed.append(time.time() - StartTime)
		# print result
		#print "------------------------------------------"
		time.sleep(delay)

	#spi.close()
	print "Delay Time = %r"%delay
	print "Actual sample points recored in 10 seconds: %r"%(len(temp_level))
	return temp_level,time_elapsed
	




