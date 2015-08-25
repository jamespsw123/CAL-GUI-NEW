# Code of the solenoid control, in cooperation with the adc mcp3008 which is used for reading the 
# potentiometer.

import RPi.GPIO as GPIO
# assume a sample lengh as 10"
sample_len = 254
# define hte potentiometer channel on MCP3008
poten_channel = 2
# pin definition for the solenoids
Solenoid_Pin_1 = 11
Solenoid_Pin_2 = 13
Solenoid_Pin_3 = 15
# position definition of gates
Gate_1_pos = 
Gate_2_pos = 
Gate_3_pos = 
# define a safety clearance before the sample hits the gate
safety_clearance = 
# pin setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(Solenoid_Pin_1, GPIO.OUT)
GPIO.setup(Solenoid_Pin_2, GPIO.OUT)
GPIO.setup(Solenoid_Pin_3, GPIO.OUT)
# Initial state for LEDs:
GPIO.output(Solenoid_Pin_1, GPIO.LOW)
GPIO.output(Solenoid_Pin_2, GPIO.LOW)
GPIO.output(Solenoid_Pin_3, GPIO.LOW)

# read the potentiometer and conevert it in to distance
def read_poten(channel):
	data = ReadChannel_10bit(channel) # ReadChannel is defined in FastRead.py, assume thermocouple is on channel 0
	volt = ConvertVolts_10bit(data, 3)
	## use volt above to calculate the position of the sample

	return sample_pos

def gate_control(direction, sample_position, Gate_pos, Solenoid_Pin):
	if direction == 1 and not GPIO.input(Solenoid_Pin): # while the sample is moving upwards
		if sample_position > (Gate_pos - safety_clearance) and \
		sample_position < (Gate_pos + sample_len):
			GPIO.output(Solenoid_Pin, 1)

	elif direction == 1 and GPIO.input(Solenoid_Pin):
		if sample_position > (Gate_pos + safety_clearance + sample_len):
			GPIO.output(Solenoid_Pin, 0)

	elif direction == 0 and not GPIO.input(Solenoid_Pin):# while the sample is moving downwards
		if sample_position < (Gate_pos + safety_clearance) and \
		sample_position > (Gate_pos - sample_len):
			GPIO.output(Solenoid_Pin, 1)

	elif direction == 0 and GPIO.input(Solenoid_Pin):
		if sample_position < (Gate_pos - safety_clearance - sample_len):
			GPIO.output(Solenoid_Pin, 0)


def solenoid_thread():
	# start a thread in main()
	# thread = threading.Thread(target = solenoid_thread, name = "solenoid control")
	# thread.start()

	# in main():
	# solenoid_position[0] = read_poten(poten_channel)
	# solenoid_position.append(None)

	# solenoid_position is a list that passed down from the main thread
	# solenoid_switch is a flag, it should be set True whenever the main thread is quit
	global solenoid_switch,solenoid_position
	# lock is used to make sure that the first position passed from the main thread is correct
	# define the lock in main()
	# lock = threading.Lock()
	lock.acquire()
	try: 
		while not solenoid_switch:
			direction = 3 # indicator of the sample moving direction
			sample_position[1] = read_poten(poten_channel)
			if sample_position[1] > sample_position[0]:
				direction = 1 # this means sample is moving upward
			elif sample_position[1] < sample_position[0]:
				direction = 0 # this means sample is moving downward
			
			gate_control(direction, sample_position[1], Gate_1_pos, Solenoid_Pin_1)
			gate_control(direction, sample_position[2], Gate_2_pos, Solenoid_Pin_2)
			gate_control(direction, sample_position[3], Gate_3_pos, Solenoid_Pin_3)
	finally:
		lock.release()





