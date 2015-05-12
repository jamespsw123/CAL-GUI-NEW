# send data to oven
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

def setTemp(slave, temps1):
	Master_Number = "01"
	Slave_Address = dig_convert(slave, 2)
	Function_Code = "WRW"
	Time_Delay = "0"
	Register_Type = "D"
	Number_of_Words = dig_convert(len(temps1), 2)
	Message = ""
	for i in range(len(temps1)):
		Register_Number = dig_convert(str(114 + i), 4) + " "
		if i == len(temps1) -1 :
			Message += Register_Type + Register_Number + str(hex_convert(temps1[i])).upper()
		else:
			Message += Register_Type + Register_Number + str(hex_convert(temps1[i])).upper() + " "
	return STX+Slave_Address+Master_Number+Time_Delay+Function_Code+Number_of_Words+Message+ETX+CR

def setInterval(slave, interval):
	Master_Number = "01"
	Slave_Address = dig_convert(slave, 2)
	Function_Code = "WRW"
	Time_Delay = "0"
	Register_Type = "D"
	Number_of_Words = dig_convert(len(interval), 2)
	Message = ""
	for i in range(len(interval)):
		Register_Number = dig_convert(str(201 + i), 4) + " "
		if i == len(interval) -1 :
			Message += Register_Type + Register_Number + str(hex_convert(interval[i])).upper()
		else:
			Message += Register_Type + Register_Number + str(hex_convert(interval[i])).upper() + " "
	return STX+Slave_Address+Master_Number+Time_Delay+Function_Code+Number_of_Words+Message+ETX+CR

def getPV(slave, port):
	Master_Number = "01"
	Slave_Address = dig_convert(slave, 2)
	Function_Code = "WRD"
	Time_Delay = "0"
	Register_Type = "D"
	Number_of_Words = "01"
	Message = STX+Slave_Address+Master_Number+Time_Delay+Function_Code+Register_Type+"0002"+","+\
		Number_of_Words +ETX+CR
	print Message[1:]
	port.write(Message)
	receive = readlineCR(port)
	return receive

def Reset(slave, port):
	Master_Number = "01"
	Slave_Address = dig_convert(slave, 2)
	Function_Code = "WWR"
	Time_Delay = "0"
	Register_Type = "D"
	Number_of_Words = "01"
	Message = STX+Slave_Address+Master_Number+Time_Delay+Function_Code+Register_Type+"0121"+","+\
		Number_of_Words+ ",0001" +ETX+CR
	print Message[1:]
	port.write(Message)
	receive = readlineCR(port)
	return receive

def Run(slave, port):
	Master_Number = "01"
	Slave_Address = dig_convert(slave, 2)
	Function_Code = "WWR"
	Time_Delay = "0"
	Register_Type = "D"
	Number_of_Words = "01"
	Message = STX+Slave_Address+Master_Number+Time_Delay+Function_Code+Register_Type+"0121"+","+\
		Number_of_Words+ ",0001" +ETX+CR
	print Message[1:]
	port.write(Message)
	receive = readlineCR(port)
	return receive

def getSTATUS(slave, port):
	Master_Number = "01"
	Slave_Address = dig_convert(slave, 2)
	Function_Code = "WRD"
	Time_Delay = "0"
	Register_Type = "D"
	Number_of_Words = "01"
	Message = STX+Slave_Address+Master_Number+Time_Delay+Function_Code+Register_Type+"0001"+","+\
		Number_of_Words +ETX+CR
	print Message[1:]
	port.write(Message)
	receive = readlineCR(port)
	return receive

def getCSP(slave, port):
	Master_Number = "01"
	Slave_Address = dig_convert(slave, 2)
	Function_Code = "WRD"
	Time_Delay = "0"
	Register_Type = "D"
	Number_of_Words = "01"
	Message = STX+Slave_Address+Master_Number+Time_Delay+Function_Code+Register_Type+"0003"+","+\
		Number_of_Words +ETX+CR
	print Message[1:]
	port.write(Message)
	receive = readlineCR(port)
	return receive

def readlineCR(port):
	rv = ""
	while 1:
		ch = port.read()
		rv += ch
		if ch == '\r' or ch == CR:
			return rv


print getPV(01, ser)[7:11]
#print Reset(01, ser)[1:]
"""

temps1 = [20]
interval = [1000, 3000]

send1 = setTemp(01, temps1)
send2 = setInterval(01, interval)

ser.write(send1)
print send1[1:]
receive = readlineCR(ser)
print receive[1:]


#ser.write(send2)
#print send2[1:]
#receive = readlineCR(ser)
#print receive[1:]
#print Run(01, ser)[1:]
print getSTATUS(01, ser)[1:]
print getCSP(01, ser)[1:]
"""


