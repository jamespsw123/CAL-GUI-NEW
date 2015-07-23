# fast reading data
import spidev
import time
import os

# Open SPI bus
spi = spidev.SpiDev()
spi.open(0,0)

# Define sensor channel
TMP36 = 1

# Function to read SPI data from MCP3008 chip
def ReadChannel(channel):
	adc = spi.xfer2([1,(8+channel)<<4,0])
	data = ((adc[1]&3)<<8)+adc[2]
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
delay = 1
# Define the length of the test
length = 5

# Start the test
StartTime = time.time()
while (time.time() - StartTime < length):
	temp_level = ReadChannel(TMP36)
	temp_volts = ConvertVolts(temp_level,2)
	temp = ConvertTemp_TMP36(temp_level,2)
	# print result
	print "------------------------------------------"
	print("Temp : {} ({}V) {} deg C".format(temp_level,temp_volts,temp))
time.sleep(delay)