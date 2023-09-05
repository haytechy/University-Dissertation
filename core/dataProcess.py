import pickle
import os
import random
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
        return False

def getSampleSize(fileName):
    data = readData(fileName)
    if data:
        return len(data)
    else:
        return False

def getPermissionsFrequncy(fileName, size):
    permissionFrequency = Counter()
    data = readData(fileName)
    if data:
        random.shuffle(data)
        for application in data[:size]:
            permissionFrequency += Counter(application['permissions'])
    return permissionFrequency

def getClassesFrequency(fileName, size):
    classTypes = ['internal', 'external', 'all']
    classFrequency = {'internal': Counter(), 'external': Counter(), 'all': Counter()}
    data = readData(fileName)
    if data:
        random.shuffle(data)
        for application in data[:size]:
            for types in classTypes:
                classFrequency[types] += Counter(application[types])
    return classFrequency
