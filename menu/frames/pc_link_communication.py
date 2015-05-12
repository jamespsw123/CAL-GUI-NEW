# send data to oven
STX = chr(2)
ETX = chr(3)
CR = chr(13)

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
	# it seems that the temperature need to be amplified by 10 because of the decimal point
	temps1 = [x*10 for x in temps1]
	# above line may not needed

	for i in range(len(temps1)):
		Register_Number = dig_convert(str(230 + 2*i -1), 4) + ","
		if i == len(temps1) -1 :
			Message += Register_Type + Register_Number + str(hex_convert(temps1[i]))
		else:
			Message += Register_Type + Register_Number + str(hex_convert(temps1[i])) + ","
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
		Register_Number = dig_convert(str(231 + 2*i -1), 4) + ","
		if i == len(interval) -1 :
			Message += Register_Type + Register_Number + str(hex_convert(interval[i]))
		else:
			Message += Register_Type + Register_Number + str(hex_convert(interval[i])) + ","
	return STX+Slave_Address+Master_Number+Time_Delay+Function_Code+Number_of_Words+Message+ETX+CR


ser = serial.Serial(
				port = '/dev/ttyUSB0',
				baudrate = 9600,
				bytesize = serial.EIGHTBITS,
				parity = serial.PARITY_NONE,
				stopbits = serial.STOPBITS_ONE,
				timeout = 0.2
				)

temps1 = [100, 300 , 600, 1000, 1000, 600, 400, 300, 300, 100]
interval = [1000, 3000, 5000, 2600, 3600, 7200]

send1 = setTemp(01, temps1)
send2 = setInterval(02, interval)

ser.write(send1)
