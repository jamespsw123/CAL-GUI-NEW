# CAL-GUI-NEW

This library is used to control the CAL system at the University of Pittsburgh Swanson School of Engineering. It is designed to be run on a Raspberry Pi.

## Dependencies
- [wxPython](http://www.wxpython.com)
- [spidev](https://pypi.python.org/pypi/spidev)
- [numpy](http://www.numpi.org)
- [matplotlib](http://matplotlib.org/)
- [smbus](https://pypi.python.org/pypi/smbus-cffi/0.4.1)

## Introduction
In order to make the whole system run automatically, the CAL system is controlled by the raspberry pi as its micro-controller, which has a GUI written in Python with the help of wxpython and matplotlib. An Arduino is used for the control of the Stepper motor driver(TB6560) and the solenoid gates, and the communication between Arduino and Raspberry pi is via I2C. The RPI communicates with the furnaces(TF55030C) via Serial interface. The protocol used between the RPI and the furnaces is called "PC Link communication", which is developed by the furnaces temp-controller provider, Yokogawa. The RPI also communicates with the temperature detection module in SPI protocol. The module is consists of an ADC(MCP3208 OR MCP3008), and two infrared sensors(PSG-42N and Sirius SI23). 

