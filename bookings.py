#!/usr/bin/python
import MySQLdb as mariadb
import json



mariadb_connection = mariadb.connect(user='root', password='qwerty', database='waivecar')
cursor = mariadb_connection.cursor()
cursor.execute("select * from booking_details where type='end' and created_at > '2018-04-01' order by id;") #desc limit 40;")


location = []

for booking in cursor:
    #print(booking)
    location += [(booking[3], booking[4], 1)]


with open('points-new.js', 'w') as outfile:  
    outfile.write("{}{}".format("var points=", json.dumps(location)))
        
#print(location)
print(len(location))

mariadb_connection.close()




