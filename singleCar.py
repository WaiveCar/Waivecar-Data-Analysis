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

data = json.loads(line)
ID = data['id']
current = ID

fuelPoints = []
timeStamps = []

print(ID)

while line:
    data = json.loads(line)
    if 'id' in data:
        current = data['id']
    
    if 'fuel_level' in data and current == ID:
        fuel = data['fuel_level']
        fuelPoints += [fuel]    
        
        ts = data["position"]["timestamp"]
        yourdate = dateutil.parser.parse(ts) 
        now_pacific = yourdate.astimezone(timezone('US/Pacific'))
        time = now_pacific.hour * 100 + (now_pacific.minute * 100/60)
        timeStamps += [time]   
        
    
    line = f.readline()
    
    
plt.scatter(timeStamps, fuelPoints, s=.1)
plt.ylabel('fuel level')
plt.xlabel('Date')
plt.show()

f.close()