from datetime import datetime
import json
from pprint import pprint
import matplotlib.pyplot as plt
from dateutil import tz
from datetime import datetime
from pytz import timezone
import dateutil.parser


f = open(r"C:\Users\shira\Desktop\WaiveCar\serv1\log.txt.4", "r", newline='\n')
line = f.readline()


fuelPoints7 = []
fuelPoints10 = []
fuelPoints13 = []
fuelPoints16 = []
fuelPoints19 = []

timeStamps = []
carCount = [ set() for x in range(0, 5) ]

while line:
    data = json.loads(line)
    
    
    if 'fuel_level' in data  and 'electric_vehicle_state' in data: #and data['immobilizer'] == 'unlocked':
        ts = data["t"]
        yourdate = dateutil.parser.parse(ts) 
        now_pacific = yourdate.astimezone(timezone('US/Pacific'))
        time = now_pacific.hour * 100 + (now_pacific.minute * 100/60)        
        if time >= 700 and time < 750:
            time = (time//100) * 100
            
            timeStamps += [time]         
            fuel = data['fuel_level']
            #print("Fuel level: " + str(fuel))
            fuelPoints7 += [fuel]
            carCount[0].add(data['id'])
        if time >= 1000 and time < 1050:
            time = (time//100) * 100
            
            timeStamps += [time]         
            fuel = data['fuel_level']
            #print("Fuel level: " + str(fuel))
            carCount[1].add(data['id'])
            fuelPoints10 += [fuel]        
        if time >= 1300 and time < 1350:
            time = (time//100) * 100
            
            timeStamps += [time]         
            fuel = data['fuel_level']
            #print("Fuel level: " + str(fuel))
            fuelPoints13 += [fuel]  
            carCount[2].add(data['id'])
            
        if time >= 1600 and time < 1650:
            time = (time//100) * 100
            
            timeStamps += [time]         
            fuel = data['fuel_level']
            #print("Fuel level: " + str(fuel))
            fuelPoints16 += [fuel] 
            carCount[3].add(data['id'])
            
        if time >= 1900 and time < 1950:
            time = (time//100) * 100
            
            timeStamps += [time]         
            fuel = data['fuel_level']
            #print("Fuel level: " + str(fuel))
            fuelPoints19 += [fuel]
            carCount[4].add(data['id'])
            
    line = f.readline()
    
hourly = [fuelPoints7, fuelPoints10, fuelPoints13, fuelPoints16, fuelPoints19]
print("{}".format(','.join([ str(len(x)) for x in carCount])))

plt.boxplot(hourly)
plt.ylabel('fuel level')
plt.xlabel('Time')
plt.show()

f.close()
