#!/usr/bin/python
import MySQLdb
import time

#Connect to database
db = MySQLdb.connect(host = 'localhost', port = 3306, user = 'root', passwd = 'Python')
#Password is set when MySQL is installed.
cursor = db.cursor()

#Initialize database
def dbInit():
	a = cursor.execute("show databases like 'record'")
	if a == 1:
		cursor.execute("drop database record")
	cursor.execute("create database record")
	cursor.execute("use record")

	cursor.execute("create table test(time char(20), temp int(4), C_temp int(4), adc_temp int(4))")
	cursor.execute("create table cooling(time char(20), temp int(4))")

#Write to database
def dbWrite1(time, temp, C_temp, adc_temp):
	cursor.execute("""insert into test(
		time, temp, C_temp, adc_temp) values(%s, %s, %s, %s)""", (time, temp, C_temp, adc_temp))
	db.commit()

def dbWrite2(time, temp):
	cursor.execute("""insert into cooling(
		time, temp) values(%s, %s)""", (time, temp))
	db.commit()

#Outfile
def dbOut():
	time1 = time.strftime("%m%d%Y %H%M%S")
	cursor.execute("""select time, temp, C_temp, adc_temp into outfile
		"/tmp/test %s.txt"
		lines terminated by "\r\n"
		from test""" % (time1))
	cursor.execute("""select time, temp into outfile
		"/tmp/cooling %s.txt"
		lines terminated by "\r\n"
		from cooling""" % (time1))
#Export the data wehn recording is finished.
#Make sure the folder "D:/CAL Project" exists.

dbInit()
dbWrite1(1, 2, 3, 4)
dbWrite2(5, 6)
dbOut()