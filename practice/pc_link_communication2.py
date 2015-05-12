import serial
STX = chr(2)
ETX = chr(3)
CR = chr(13)

ser = serial.Serial(
				port = '/dev/ttyUSB0',
				baudrate = 9600,
				bytesize = serial.EIGHTBITS,
				parity = serial.PARITY_EVEN,
				stopbits = serial.STOPBITS_ONE,
				timeout = 0.2
				)
def getUPR(slave, port):
	port.write(STX+slave+"010WRDD0201,01"+ETX+CR)
	return  readlineCR(port)

def getDNR(slave, port):
	port.write(STX+slave+"010WRDD0202,01"+ETX+CR)
	return  readlineCR(port)

def dig_convert(number, n):
	number = str(number)
	while len(number) < n:
		number = '0' + number
	return number

def hex_convert(number):
	number = hex(number)[2:]
	if len(number) > 4 :
		print "Value more than FFFF, invalid"
	else:
		while len(number) < 4:
			number = '0' + number
		#print number
		return number
def readlineCR(port):
	rv = ""
	while 1:
		ch = port.read()
		rv += ch
		if ch == '\r' or ch == CR:
			return rv

def getPV(slave, port):
	"""
	Master_Number = "01"
	Slave_Address = dig_convert(slave, 2)
	Function_Code = "WRD"
	Time_Delay = "0"
	Register_Type = "D"
	Number_of_Words = "01"

	Message = STX+Slave_Address+Master_Number+Time_Delay+Function_Code+Register_Type+"0002"+","+\
		Number_of_Words +ETX+CR
	"""
	#Message = STX+dig_convert(slave, 2)+"010WRDD000201"+ETX+CR
	#print Message[1:]
	port.write(STX+slave+"010WRDD0002,01"+ETX+CR)
	receive = readlineCR(port)
	return receive

def setTemp(slave, temps1, port):
	
	#Master_Number = "01"
	Slave_Address = dig_convert(slave, 2)
	"""
	Function_Code = "WRW"
	Time_Delay = "0"
	Register_Type = "D"
	Number_of_Words = "01"
	Message = ""
	Register_Number = dig_convert(str(114), 4) + " "
	Message = Register_Type + Register_Number + str(hex_convert(temps1[i])).upper()
	"""
	#return STX+Slave_Address+Master_Number+Time_Delay+Function_Code+Number_of_Words+Message+ETX+CR
	message = STX+Slave_Address+"01"+"0"+"WRW"+"01"+"D0114,"+str(hex_convert(temps1)).upper()+ETX+CR
	port.write(message)
	print readlineCR(port)
	



def setRamp(slave, Ramp, UD, port):
	#Master_Number = "01"
	Slave_Address = dig_convert(slave, 2)
	if UD == 1:
		D_Register = "D0201,"
		message =  STX+Slave_Address+"01"+"0"+"WRW"+"01"+D_Register+str(hex_convert(Ramp)).upper()+ETX+CR
		message2 =  STX+Slave_Address+"01"+"0"+"WRW"+"01"+"D0202,"+str(hex_convert(Ramp)).upper()+ETX+CR
		print "setramp:"
		port.write(message)
		print readlineCR(port)[1:]
		port.write(message2)
		print readlineCR(port)[1:]
	elif UD == -1:
		D_Register = "D0202,"
		message =  STX+Slave_Address+"01"+"0"+"WRW"+"01"+D_Register+str(hex_convert(Ramp)).upper()+ETX+CR
		message2 =  STX+Slave_Address+"01"+"0"+"WRW"+"01"+"D0201,"+str(hex_convert(Ramp)).upper()+ETX+CR
		port.write(message)
		print readlineCR(port)[1:]
		port.write(message2)
		print readlineCR(port)[1:]
	

setRamp(01, 100, -1, ser)
#print getDNR("01", ser)[1:]

setTemp(01, 50, ser)
hex_temp = getPV("01", ser)[7:11]
temp = int(hex_temp,16)
print "current temp:" 
print temp
#print getPV("01", ser)