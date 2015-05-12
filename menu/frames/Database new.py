#!/usr/bin/python
import MySQLdb

db = MySQLdb.connect(host = 'localhost', port = 3306,
	user = 'root', passwd = 'Python')
#The password is set when MySQL is installed.
cursor = db.cursor()

#Database initialization
def dbInit(order):
	a = cursor.execute("show databases like 'record'")
	if a == 0:
		cursor.execute("create database record")

	cursor.execute("use record")

	b = cursor.execute("show tables like 'temperature%s'" % (order))
	if b == 0:
		cursor.execute("""create table temperature%s(
			id int(6) not null primary key auto_increment,
			time char(20),
			sec int(6),
			temp int(4)
			)""" % (order))
	else:
		cursor.execute("truncate table temperature%s" % (order))
#"order" is the order number to create different tables for different samples.

#Write to database
def dbWrite(order, time1, sec1, temp1):
	cursor.execute("insert into temperature%s(time, sec, temp) values(%s, %s, %s)", (order, time1, sec1, temp1))
	db.commit()
#Add to the main cycle to record the time, the interval
#and the temperature in the database for each point.

#Read from database
def dbRead(order):
	cursor.execute("select * from temperature%s" % (order))
	results = cursor.fetchall()
	Listdb = []
	for row in results:
		secn = int(row[2])
		tempn = int(row[3])
		Listdb.append((secn,tempn))
	return Listdb
#Add to the main cycle to renew the list of intervals
#and the list of temperatures when needed.

#Outfile
def dbOut(order):
	cursor.execute("""select id, time, sec, temp into outfile
		"D:/CAL Project/temperature%s.txt"
		lines terminated by "\r\n"
		from temperature%s
		""", (order, order))
#Export the data when recording is finished.
#Make sure the folder "D:/CAL Project" exists.

#Clearance if needed
def dbClear(order):
	#cursor.execute("drop table temperature%s" % (order))		#Clearance of table
	#cursor.execute("drop database record")					#Clearance of database
	cursor.close()		#Close the cursor
	db.close()			#Disconnect from the database



#Test of the database
import time

order = 1
dbInit(order)
i = 0
while i <= 9:
	time1 = "00:00:0" + str(i)
	sec1 = i
	temp1 = 20 + i
	dbWrite(order, time1, sec1, temp1)
	print dbRead(order)
	i += 1
	time.sleep(0.5)
dbOut(order)
dbClear(order)