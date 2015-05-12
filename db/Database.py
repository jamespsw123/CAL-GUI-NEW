#!/usr/bin/python
import MySQLdb

db = MySQLdb.connect(host = 'localhost', port = 3306,
	user = 'root', passwd = 'cal')
cursor = db.cursor()

#Database initialization starts.
a = cursor.execute("show databases like'record'")
if a == 0:
	cursor.execute("create database record")

cursor.execute("use record")

b = cursor.execute("show tables like 'temperature'")
if b == 0:
	cursor.execute("""create table temperature(
		id int not null primary key auto_increment,
		time char(20),
		sec int,
		temp int
		)""")
else:
	cursor.execute("truncate table temperature")
#Database initialization ends.

#Data for test
time1 = "09:09:09"
sec1 = 9
temp1 = 27

#Record
sql = "insert into temperature(time, sec, temp) values(%s, %s, %s)"
cursor.execute(sql, (time1, sec1, temp1))
db.commit()
#Add to the main cycle to record the time, the interval
#and the temperature in the database every second.

#Outfile

cursor.execute("""select id, time, sec, temp into outfile
	"Desktop record.txt"
	lines terminated by "\r\n"
	from temperature
	""")
#Export the data when recording is finished.
#Make sure the folder "D:/CAL Project" exists.

#Clearance if needed.
cursor.execute("drop table temperature")
cursor.execute("drop database record")

#Disconnect from the database.
cursor.close()
db.close()