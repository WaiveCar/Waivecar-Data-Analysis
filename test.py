from datetime import datetime
import json
from pprint import pprint
import matplotlib.pyplot as plt
from dateutil import tz
from datetime import datetime
from pytz import timezone
import dateutil.parser


f = open(r"C:\Users\shira\Desktop\WaiveCar\serv1\log.txt", "r", newline='\n')
line = f.readline()


fuelPoints = []
timeStamps = []
#for i in range(5):
while line:
    data = json.loads(line)
    
    
    if 'fuel_level' in data:
        fuel = data['fuel_level']
        #print("Fuel level: " + str(fuel))
        fuelPoints += [fuel]
       
        ts = data["position"]["timestamp"]
        yourdate = dateutil.parser.parse(ts) 
        now_pacific = yourdate.astimezone(timezone('US/Pacific'))
        #time = now_pacific.hour * 60 + now_pacific.minute
        time = now_pacific.hour * 100 + (now_pacific.minute * 100/60)
        timeStamps += [time] 
        
    line = f.readline()
 
   

plt.scatter(timeStamps, fuelPoints, s=.1)
plt.ylabel('fuel level')
plt.xlabel('Date')
plt.show()

f.close()