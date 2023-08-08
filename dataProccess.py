import pickle
from collections import Counter

def loadFile(dataFile):
    with open(dataFile, "rb") as f:
        data = pickle.load(f)
    return data

def getPermissionsFrequncy(data):
    permissionFrequency = Counter()
    for application in data:
        permissionFrequency += Counter(application['permissions'])
    print(permissionFrequency.most_common(20))


def getClassFrequency(dataFile):
    with open(dataFile, "rb") as f:
        classesData = pickle.load(f)

    print(classesData[0]["hash"])
