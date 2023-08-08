#import matplotlib.pyplot as plt
#import json
#
#with open("permissions.json", "r") as f:
#    data = json.load(f)
#
#with open("pastPermissions.json", "r") as f:
#    data2 = json.load(f)
#
#with open("pastPermissions.json", "r") as f:
#    data3 = json.load(f)
#
#permissions = list(data.keys())[:10]
#frequency = list(data.values())[:10]
#
#plt.figure(1)
#plt.bar(permissions, frequency)
#plt.tick_params(axis='x', labelsize=6)
#plt.legend()
#
#permissions = list(data2.keys())[:10]
#frequency = list(data2.values())[:10]
#
#plt.figure(2)
#plt.bar(permissions, frequency)
#plt.tick_params(axis='x', labelsize=6)
#plt.legend()
#
#permissions = list(data3.keys())[:10]
#frequency = list(data3.values())[:10]
#
#plt.figure(3)
#plt.bar(permissions, frequency)
#plt.tick_params(axis='x', labelsize=6)
#plt.legend()
#
#plt.show()
