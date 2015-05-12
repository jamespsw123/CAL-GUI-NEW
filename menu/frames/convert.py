# Convert a number to a 4-digit character string
def hex_convert(number):
	number = hex(number)[2:]
	if len(number) > 4 :
		print "Value more than FFFF, invalid"
	else:
		while len(number) < 4:
			number = '0' + number
		print number
		return number
		
def dig_2(number):
	number = str(number)
	while len(number) < 2:
		number = '0' + number
	return number


hex_convert(50000)
print dig_2(3)