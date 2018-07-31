#!/usr/bin/python
import MySQLdb as mariadb
import json
import matplotlib.pyplot as plt




mariadb_connection = mariadb.connect(user='root', password='qwerty', database='waivecar')
cursor = mariadb_connection.cursor()
cursor.execute("select * from bookings where created_at > '2018-06-14' and created_at < '2018-06-20' order by user_id asc;")# limit 800;")


usersParkCount = {}
usersDriveCount = {}
usersTotalCount = {}

for booking in cursor:
    #print(booking)
    userId = booking[1]
    if userId in usersDriveCount:
        usersDriveCount[userId] += [booking[7]]
    else:
        usersDriveCount[userId] = [booking[7]]
        
        
    if userId in usersParkCount:
        usersParkCount[userId] += [booking[8]]
    else:
        usersParkCount[userId] = [booking[8]]
        
    if userId in usersTotalCount:
        usersTotalCount[userId] += booking[7]
        usersTotalCount[userId] += booking[8]
    else:
        usersTotalCount[userId] = booking[7]
        usersTotalCount[userId] += booking[8]
    


print(usersDriveCount)
print(usersParkCount)
print(usersTotalCount)
for key in usersTotalCount.keys():
    if usersTotalCount[key]:
        if sum(usersParkCount[key])/usersTotalCount[key] > .8:
            print("{}: {} {}".format(key, usersTotalCount[key], sum(usersParkCount[key])/usersTotalCount[key]))
        
        
        
users = []
i = 1
parkRatio = []
for key in usersTotalCount.keys():
    if usersTotalCount[key] and len(usersParkCount[key]) > 4:
        users += [i]
        parkRatio += [sum(usersParkCount[key])/usersTotalCount[key]]
        i+=1
print(len(parkRatio))
plt.subplot(2, 1, 1)
plt.hist(parkRatio, bins=[.1, .2, .3, .4, .5, .6, .7, .8, .9, 1], edgecolor = 'black')

plt.ylabel("Frequency")
plt.xlabel("Park Count Ratio")
plt.tight_layout()

cursor.execute("select * from bookings where created_at > '2018-06-14' and created_at < '2018-06-26' order by user_id asc;")# limit 800;")


usersParkCount = {}
usersDriveCount = {}
usersTotalCount = {}

for booking in cursor:
    #print(booking)
    userId = booking[1]
    if userId in usersDriveCount:
        usersDriveCount[userId] += [booking[7]]
    else:
        usersDriveCount[userId] = [booking[7]]
        
        
    if userId in usersParkCount:
        usersParkCount[userId] += [booking[8]]
    else:
        usersParkCount[userId] = [booking[8]]
        
    if userId in usersTotalCount:
        usersTotalCount[userId] += booking[7]
        usersTotalCount[userId] += booking[8]
    else:
        usersTotalCount[userId] = booking[7]
        usersTotalCount[userId] += booking[8]
    


print(usersDriveCount)
print(usersParkCount)
print(usersTotalCount)
for key in usersTotalCount.keys():
    if usersTotalCount[key]:
        if sum(usersParkCount[key])/usersTotalCount[key] > .8:
            print("{}: {} {}".format(key, usersTotalCount[key], sum(usersParkCount[key])/usersTotalCount[key]))
        
        
        
users = []
i = 1
parkRatio = []
for key in usersTotalCount.keys():
    if usersTotalCount[key] and len(usersParkCount[key]) > 4:
        users += [i]
        parkRatio += [sum(usersParkCount[key])/usersTotalCount[key]]
        i+=1
plt.subplot(2.2, 1, 2)
plt.hist(parkRatio, bins=[.1, .2, .3, .4, .5, .6, .7, .8, .9, 1], edgecolor = 'black')
plt.ylabel("Frequency")
plt.xlabel("Drive Count Ratio")
plt.tight_layout()
plt.show()

#print(sum(usersParkCount[15135])/usersTotalCount[15135])

plt.savefig("userCount.png")

mariadb_connection.close()