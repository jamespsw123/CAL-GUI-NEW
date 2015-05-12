import smbus

bus = smbus.SMBus(1)
device = 0x04 

def StringToBytes(data):
	retVal = []
	for c in data:
		retVal.append(ord(c))
	return retVal

while True:

	cmd = input("Please enter cmd: ")
	if not cmd:
		continue
	data = input("Please enter data:")
	if not data:
		continue
	Data = StringToBytes(data)

	bus.write_i2c_block_data(device, cmd, Data)
	time.sleep(1)
	

