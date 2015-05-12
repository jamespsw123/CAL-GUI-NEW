# fast reading data
import spidev
import time
import os

# Open SPI bus
spi = spidev.SpiDev()
spi.open(0,0)

# Define sensor channel
LIGHT = 0
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
delay = 0.01
# Define the length of the test
length = 5.1

# Start the test
StartTime = time.time()
i = 0
while (time.time() - StartTime <= length):
	# Read the light sensor data
	light_level = ReadChannel(LIGHT)
	light_volts = ConvertVolts(light_level,2)

	temp_level = ReadChannel(TMP36)
	temp_volts = ConvertVolts(temp_level,2)
	temp = ConvertTemp_TMP36(temp_level,2)
	# print result
	#print "------------------------------------------"
	print i
	#print("Light: {} ({}V)".format(light_level,light_volts))
	print("Temp : {} ({}V) {} deg C".format(temp_level,temp_volts,temp))
	i += 1
	time.sleep(delay)



