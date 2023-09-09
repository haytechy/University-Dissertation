import numpy as np
import matplotlib.pyplot as plt
from core.dataProcess import readData, average

times = readData('data/Benchmark/times.pkl')
categories = []
averageTime = {}
timeCategory = []
decompileTime = []
droidTimes = []
androTimes = []

if times:
    for time in times:
        size = time['sampleSize']
        averageTime[size] = {"decompileTime": [], "droidloader": [], "androguard": []} 
    for time in times: 
        size = time['sampleSize']
        decompile = time['decompileTime']
        droid = time['droidloader']
        andro = time['androguard']
        averageTime[size]['decompileTime'].append(decompile)
        averageTime[size]['droidloader'].append(droid)
        averageTime[size]['androguard'].append(andro)
    for size, time in averageTime.items(): 
        timeCategory.append(size)
        decompileTime.append(average(time['decompileTime']))
        droidTimes.append(average(time['droidloader']))
        androTimes.append(average(time['androguard']))
          
x = np.arange(len(timeCategory))

barWidth = 0.3
plt.bar(x - barWidth/2, decompileTime, barWidth, label=f"Droidloader Decompile Time")
plt.bar(x - barWidth/2, droidTimes, barWidth, label=f"Droidloader Extraction Time", bottom=decompileTime)
plt.bar(x + barWidth/2, androTimes, barWidth, label=f"Androguard Extraction Time")

plt.xlabel('Sample Size')
plt.ylabel(f'time (Seconds)')
plt.title(f'Peformance between Droidloader and Androguard')
plt.xticks(x, timeCategory)
plt.legend()
plt.show()
