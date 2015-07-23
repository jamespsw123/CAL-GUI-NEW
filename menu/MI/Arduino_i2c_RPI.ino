#include <Wire.h>
#include "AccelStepper.h"


#define SLAVE_ADDRESS 0x04
#define LED (buffer1 == "L" && buffer2 == "001") // control led 13, which is on board
#define STM (buffer1 == "S") // stepper motor fucntion selected
#define gate1 700     // the hight of solenoid gate 1
#define gate2 1000	// the hight of solenoid gate 2

AccelStepper stepper(1, 9, 8); // define a stepper motor using pin 9(step) and 8(dir)

int index2;
int index3;
int position_num;
char cmd[128];	// data received will be stored in this char array
int cmdl; //data length
char sendData[128];
int index;
int start = 1;


String buffer1 = ""; // recgonise which part1 rpi trying to reach
String buffer2 = ""; // recgonise the function will be implemented
String buffer3 = ""; // recgonize what data is used
String distance = "";
String motorSpeed = "";

int Distance; // Record the number of steps we've taken
int Speed;
boolean ifbuffer1;





void setup(){
	stepper.setAcceleration(1000);
  	// led setup
	pinMode(13, OUTPUT);
	pinMode(5, OUTPUT); // GATE 1 RELAY PIN
	pinMode(6, OUTPUT);	// GATE 2 RELAY PIN

	// serial monitor setup
	Serial.begin(9600);
	Serial.print("Ready!");

	// initialize i2c as slavee
	Wire.begin(SLAVE_ADDRESS);
	//Wire.onReceive(receiveEvent);// receive data, and do some basic parse
	Wire.onReceive(receiveEvent);// receive data, and do some basic parse
}

void loop(){
	
	if (buffer1 == "S"){
		STM_FUNC(buffer3,buffer1);
	}

	
	//Serial.print("loop");
	//Serial.print(buffer1);
	//if (start == 1){
	Wire.onRequest(requestEvent);
	//}
	
}

// callback for receive data
void receiveEvent(int byteCount){
	ClearBuffer();
	// Store data from I2C into a char array cmd
	int receiveByte = 0; // set receiveByte to 0 for next data transmission
	while(Wire.available()){

		cmd[receiveByte] = Wire.read();
		receiveByte++;		
	}

	// Print received data on the serial monitor
	//Serial.println("data received: ");
	//Serial.println(cmd);
	cmdl = sizeof(cmd)/sizeof(int);
	
	for (index = 0; index < 10; index++ )// Analysis of received data
	{
		sendData[index] = cmd[index];
	}//strcpy(sendData, cmd); // THIS LINE DOES NOT WORK WELL
	

	//Serial.print("data send: ");
	//Serial.println(sendData);

	// Analyze received data
	//Serial.println("cmd");
	buffer1 = String(cmd[0]);
	buffer2 = String(cmd[sizeof(cmd)/sizeof(int)-1]);
	//Serial.println("buffer1:");
	//Serial.println(buffer1);
	//Serial.println("if buffer1 == S ");
	//Serial.println(buffer1 == "S");

	for (index = 1; index < sizeof(cmd)/sizeof(int); index++){
		buffer3 += String(cmd[index]);
	}
	index = 0;
	//Serial.println("cmd");
	//Serial.println(cmd);
	//Serial.println("parameter: ");
	//Serial.println(buffer3);
	

	// if buffer1 == "S", it means we are trying to control STEPPER MOTOR 
	// Get ready to next data transmission
	memset(cmd,0,sizeof(cmd)/sizeof(char)); // clear cmd
	Serial.println("cmd:");
	Serial.println(cmd);
	

}

// callback for sending data
void requestEvent() { 
	
    Wire.write(sendData[index]);
    ++index;
    if (index >= 64) {
         index = 0;
    }
}
void close_gate(int x){
	if (x == 1){
		digitalWrite(5, HIGH);
		Serial.println("Gate_1 Open"); 
	}
	else if (x == 2){
		digitalWrite(6, HIGH);
		Serial.println("Gate_2 Open");
	}

}
void open_gate(int x){
	if (x == 1){
		digitalWrite(5, LOW);
		Serial.println("Gate_1 Close");
	}
	else if (x == 2){
		digitalWrite(6, LOW);
		Serial.println("Gate_2 Close");
	}

}
// LED 13 will be lighted up for an interval according to the parameter received from I2C
void LED_LIGHT(String buffer3){
	digitalWrite(13, HIGH);
	delay(buffer3.toInt()); // use toInt() function to convert String to int, atoi() seems not working 
	digitalWrite(13, LOW);
	ClearBuffer(); // have to clear buffer or the loop() function will become a endless loop
}
// when "S" is received as control code
void STM_FUNC(String parameter, String buffer1){
	Serial.println("Running STM_FUNC");
	Serial.println("buffer3=");
	Serial.println(parameter);
	int tag1, tag2, tag3, tag4;
	for (index = 0; index < parameter.length() - 1; index++){
		if (parameter[index] == 'D'){
			tag1 = index;		
		}
		if (parameter[index] == 'S'){
			tag2 = index;		
		}
		if (parameter[index] == 'P'){
			tag3 = index;
		}
		if (parameter[index] == 'E'){
			tag4 = index;
		}
	}
	// get distance in string form
	for (index2 = 0; index2 < tag1; index2++){
		distance = distance + parameter[index2];
	}
	// get speed in string form	
	for (index3 = tag1+3; index3 < tag2; index3 ++){
		motorSpeed = motorSpeed + parameter[index3];
	}	
	position_num = parameter[tag3-1];
	Distance = distance.toInt();
	Speed = motorSpeed.toInt();
	if (parameter[(parameter.length() - 2)] == '1'){
				Distance = -Distance;
		}


	//Serial.println("*Distance:");
	//Serial.print(Distance);
	//Serial.println("Speed:");
	//Serial.print(Speed);
	//Serial.println("tag1");
	//Serial.println(tag1);
	//Serial.println("tag2");
	//Serial.println(tag2);
	//Serial.println("parameter length");
	//Serial.println(parameter.length());
	//Serial.println("direction");
	//Serial.print(parameter[(parameter.length()-2)]);

	stepper.setMaxSpeed(Speed);
	stepper.runToNewPosition(Distance);
	if (position_num == '1' or position_num == '2'){
		if (stepper.currentPosition()==int(0.95*float(gate1)*(3200/(3.14*110.3)))){
			open_gate(1);
		}
		if (stepper.currentPosition() ==int(0.95*float(gate2)*(3200/(3.14*110.3)))){
			open_gate(2);
			close_gate(1);
		}
		if (stepper.currentPosition() == int(1.3*float(gate2)*(3200/(3.14*110.3)))){
			close_gate(2);
		}
	}
	else if (position_num == '3'){
		if (stepper.currentPosition() == int(1.3*float(gate2)*(3200/(3.14*110.3)))){
			open_gate(2);
		}
		if (stepper.currentPosition() == int(0.99*float(gate2)*(3200/(3.14*110.3)))){
			close_gate(2);
		}
	}
	else if (position_num == '4'){
		open_gate(1);
		if (stepper.currentPosition() == int(0.99*float(gate1)*(3200/(3.14*110.3)))){
			close_gate(1);
		}
	}
  	Serial.println("STM_FUNC LOOP END");
  	ClearBuffer();
}
void ClearBuffer(){
	buffer1 = "";
	buffer2 = "";
	buffer3 = "";
	distance = "";
	motorSpeed = "";
}
