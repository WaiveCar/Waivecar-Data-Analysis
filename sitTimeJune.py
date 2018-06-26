#!/usr/bin/python
import MySQLdb as mariadb
import json



mariadb_connection = mariadb.connect(user='root', password='qwerty', database='waivecar')
cursor = mariadb_connection.cursor()
#cursor.execute("select * from booking_details where type='end' and created_at > '2018-04-01' order by id;")
cursor.execute("""select bookings.id, bookings.car_id, booking_details.type, booking_details.longitude,
booking_details.latitude, booking_details.created_at from bookings
join booking_details on bookings.id = booking_details.booking_id
where bookings.created_at > '2018-06-06' and bookings.created_at < '2018-06-20' 
order by car_id desc, bookings.created_at asc
;""")
  
line = cursor.fetchone()
print(line)


i = 1
endtime = 0
sitTime = []

while line:
 if i == 1:
  i+=1
  line = cursor.fetchone()
 else:
    carId = line[1]
    #print(carId)
    while line and line[1] == carId:
        if line[2] == 'end':
            endTime = line[5]
            longEnd = round(line[3], 2)
            latEnd = round(line[4], 2)
        else:
            startTime = line[5]
            timeBetween = startTime - endTime
           
            longStart= round(line[3], 2)
            latStart = round(line[4], 2)
            if longStart == longEnd and latStart == latEnd:
             sitTime += [(round(line[4]*2,2)/2, round(line[3]*2,2)/2, timeBetween.seconds)]
        i += 1
        line = cursor.fetchone()
    
    line = cursor.fetchone()
#print(sitTime)   

averages = {}
for i in sitTime:
 points = (round(i[0]*2, 2)/2 , round(i[1]*2, 2)/2)
 seconds = i[2]
 if points in averages:
  averages[points] += [seconds]
 else:
  averages[points] = [seconds]
  
for i in averages.keys():
 av = sum(averages[i])/len(averages[i])
 averages[i] = av


realSitTime= []
for i in averages.keys():
 long = i[0]
 lat = i[1]
 time = averages[i]
 realSitTime += [(long, lat, time)]
print(realSitTime)
#print(averages)


with open('points-new.js', 'w') as outfile:  
    outfile.write("{}{}".format("var points=", json.dumps(realSitTime)))
    


    
mariadb_connection.close()