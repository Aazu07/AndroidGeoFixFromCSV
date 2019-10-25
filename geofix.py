#!/usr/bin/env python
import sys
import telnetlib
from time import sleep
import csv
from datetime import datetime

#-------Emulator Host and port------------
HOST = "127.0.0.1"
PORT = 5554

#-------Device Host and port------------
# HOST = "192.168.104.9"
# PORT = 5554

#-------Change the path according to your csv file path---------
GeoFilePath = "/home/FeoFixUsingCSV/location.csv"


#---------DO NOT CHANGE ANYTHING BEYOND THIS-------------------
TIMEOUT = 10
latitude_list = []
longitude_list = []
time_list = []

#------ NEED AUTHENTICATION WHILE USING EMULATOR---------------
if(HOST == "127.0.0.1"):
    #----LOCTION OF THIS FILE ON YOUR SYSTEM---
    FILE = open('/home/.emulator_console_auth_token', 'r')
    AUTH_TOKEN = FILE.read()
    FILE.close()

reader = csv.DictReader(open(GeoFilePath))
for raw in reader:
	latitude_list.append(float(raw["lat"]))
	longitude_list.append(float(raw["lng"]))
	time_list.append(datetime.strptime(raw["created_at"], '%Y-%m-%d %H:%M:%S'))

tn = telnetlib.Telnet(HOST, PORT, TIMEOUT)
tn.set_debuglevel(9)
tn.read_until(("OK").encode('ascii'), 5)

if(HOST == "127.0.0.1"):
    tn.write(("auth {0}\n".format(AUTH_TOKEN)).encode('ascii'))
    tn.read_until(("OK").encode('ascii'), 5)

for i in range(len(latitude_list)):
    lat = latitude_list[i]
    lng = longitude_list[i]
    tn.write(("geo fix {0} {1}\n".format(lng, lat)).encode('ascii'))
    duration = 1
    if i < len(latitude_list) -1 :
    	diff = abs(time_list[i+1] - time_list[i])
    	duration = diff.total_seconds()
    sleep(duration)
tn.write(("exit\n").encode('ascii'))

print(tn.read_all())
