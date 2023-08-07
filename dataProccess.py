import pickle

def loadFile(dataFile):
    with open(dataFile, "rb") as f:
        data = pickle.load(f)
    print(data[0]["permissions"])
    return data

def getPermissions(dataFile):
    with open(dataFile, "rb") as f:
        permissionsData = pickle.load(f)
    print(permissionsData)

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
permissions = loadFile("data/testPermissions.pkl")
