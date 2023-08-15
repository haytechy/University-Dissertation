import pickle
import os
from collections import Counter

def writeData(data, dirName, fileName):
    if not os.path.exists(f"data/{dirName}"):
        os.makedirs(f"data/{dirName}")
    with open(f"data/{os.path.basename(dirName)}/{fileName}.pkl", "wb") as f:
        pickle.dump(data, f)

def readData(fileName):
    if os.path.exists(fileName):
        with open(f"{fileName}", "rb") as f:
            return pickle.load(f)
    else:
        print("Filename does not exists")
        return False

def getPermissionsFrequncy(data, limit):
    permissionFrequency = Counter()
    for application in data:
        permissionFrequency += Counter(application['permissions'])
    return permissionFrequency.most_common(limit)

def getClassesFrequency(data, classType, limit):
    classesFrequency = Counter()
    for application in data:
        classesFrequency += Counter(application[classType])
    return classesFrequency.most_common(limit)


getPermissionsFrequncy(readData("data/CICAndMal2017Decoded/permissions.pkl"), 10000)
#def getClassFrequency(data):
