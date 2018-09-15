#!/usr/bin/python
import MySQLdb as mariadb
import json
import pprint
import matplotlib.pyplot as plt
from operator import itemgetter



mariadb_connection = mariadb.connect(user='root', password='password', database='waivecar_development')
cursor = mariadb_connection.cursor()

cursor.execute("""select bookings.id, cars.license, booking_details.type, booking_details.mileage, booking_details.charge, bookings.user_id from bookings
join booking_details on bookings.id = booking_details.booking_id
join cars on bookings.car_id = cars.id
where bookings.created_at > '2018-06-01'
order by bookings.created_at asc, cars.license asc
;""")

#This matches a booking to a starting and ending mileage
mileage = {}
#This matches the bookings to a user
user = {}
for b in cursor:
    booking_id = b[0] 
    user[booking_id] = b[5]
    if b[5] in [2723,3213,8779,10453]:
        continue
    if booking_id in mileage and b[2] == 'end':
        mileage[booking_id] += [(b[3], b[2], b[1])]
    elif booking_id not in mileage and b[2] == 'start':
        mileage[booking_id] = [(b[3], b[2], b[1])]
#print('user: ', user)    
#print('mileage: ', mileage)
a = []
b = []
#This matches a booking to its distance in miles
distance = {}
for key in mileage.keys():
    if len(mileage[key]) == 2:
        d = mileage[key][1][0] - mileage[key][0][0]
        if d > 10:
            distance[key] = d
            a += [d]
        else:
            b += [d]
#print('distance: ', distance)

#This matches bookings with their charges at the starts and ends of rides
charge = {}
for b in cursor:
    booking_id = b[0] 
    if booking_id in charge and b[2] == 'end':
        charge[booking_id] += [(b[4], b[2], b[1])]
    elif booking_id not in charge and b[2] == 'start':
        charge[booking_id] = [(b[4], b[2], b[1])]
#print('charge: ', charge)

#This calculates the charge differences for bookings
chargeDifference = {}
for key in charge.keys():
    if len(charge[key]) == 2 and charge[key][1][0] and charge[key][0][0]:
        c = float(charge[key][0][0] - charge[key][1][0])
     
        if charge[key][0][2].lower() in ["waive{}".format(x) for x in range(1, 20)]:
            chargeDifference[key] = c*.70
        else:
            chargeDifference[key] = c*1.40
#print('chargeDifference: ', chargeDifference)

#This is a list of all of the diffent ratios that have been calculated
ratio = []
#This seems to be the frequencies of each user taking rides
freq = {}
for key in distance.keys():
    if key in chargeDifference and chargeDifference[key]:
        r = float(distance[key])/chargeDifference[key]
        if r > -5.5 and r < 5.5:
            ratio += [r]
        if r < -0:
            if user[key] not in freq:
                freq[user[key]] = 0
            freq[user[key]] += 1
#print('freq: ', freq.keys())
#print('ratio: ', ratio)
print(list(reversed(sorted([(user,times) for user,times in freq.items()], key=itemgetter(1)))))

#print(max(ratio))
#plt.hist(ratio, bins=[-.2, -.15, -.1, -.075, -.05, -.025, 0, .025, .05, .075, .1, .15, .2, .25], edgecolor = 'black')
plt.yscale('log', nonposy='clip')
plt.hist(ratio, bins=[float(x)/20 for x in range(-90, 90)], edgecolor = 'black')

plt.show()
plt.savefig("carCharge.png")


mariadb_connection.close()

