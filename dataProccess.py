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
    
   # for classes in classesList:
   #     classesFrequency += Counter(classes)

   # print(classesFrequency.most_common(20))

#getClassFrequency("data/CICAndMal2017DecodedClasses.pkl")
#getClassFrequency("data/MalwareBazaarRecentDecodedClasses.pkl")
#getClassFrequency("data/MalwareBazaarRecentDecodedExternelClasses.pkl")
#getClassFrequency("data/testClasses.pkl")
#permissions = loadFile("data/CICAndMal2017DecodedPermissions.pkl")
#getPermissionsFrequncy(permissions)
#permissions = loadFile("data/MalwareBazaarRecentDecodedPermissions.pkl")
#getPermissionsFrequncy(permissions)
#permissions = loadFile("data/MalwareBazaarFamilyDecodedPermissions.pkl")
#getPermissionsFrequncy(permissions)
