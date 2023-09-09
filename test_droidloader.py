from droidloader import getPermissions
from core.classAnalyser import getClasses
from core.androguardAnalyser import getPermissionsAndClasses

def testGetPermissions():
    permissions = getPermissions('datasets/TestDecoded', 10)
    androguardPermissions = getPermissionsAndClasses('datasets/Test', 10)[0]
    successful = 0
    for i in range(len(permissions)):
        for j in range(len(androguardPermissions)):
            if permissions[i]['hash'] == androguardPermissions[j]['hash']:
                successful += 1
    print(f"[+] 10 samples tested")
    print(f"[+] {successful} permissions from samples are correct compared to Androguard") 

def testGetClasses():
    classes = getClasses('datasets/TestDecoded', 10)
    androguardClasses = getPermissionsAndClasses('datasets/Test', 10)[1]
    classTypes = ['internal', 'external', 'all']
    equalScore = [0, 0, 0]
    containsScore = [0, 0, 0]
    difference = []
    total = []
    for i in range(len(classes)):
        for j in range(len(androguardClasses)):
            if classes[i]['hash'] == androguardClasses[j]['hash']:
                for k in range(len(classTypes)): 
                    if classes[i][classTypes[k]] == androguardClasses[j][classTypes[k]]:
                        equalScore[k] += 1
                    if len(androguardClasses[j][classTypes[k]] - classes[i][classTypes[k]]) == 0:
                        containsScore[k] += 1

    print(f"[+] 10 samples tested")
    for i in range(len(classTypes)):
        print(f"[+] {equalScore[i]} {classTypes[i]} classes from samples are correct compared to Androguard") 
        print(f"[+] {containsScore[i]} {classTypes[i]} clasess from samples contains classes from Androguard") 

    print(total)
    for i in range(len(total)):
        print(f" Hash: {classes[i]['hash']} Total classes: {total[i]} Difference: {difference[i]}") 

if __name__ == "__main__":
    #testGetPermissions()
    testGetClasses()
