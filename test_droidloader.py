from droidloader import getPermissions
from core.classAnalyser import getClasses
from core.androguardAnalyser import getPermissionsAndClasses

def testGetPermissions():
    permissions = getPermissions('datasets/TestDecoded', 1)
    androguardPermissions = getPermissionsAndClasses('datasets/Test', 10)[0]
    successful = 0
    for i in range(len(permissions)):
        for j in range(len(androguardPermissions)):
            if permissions[i]['hash'] == androguardPermissions[j]['hash']:
                successful += 1
    print(f"[+] 10 samples tested")
    print(f"[+] {successful} permissions from samples are correct compared to Androguard") 

def testGetClasses():
    classes = getClasses('datasets/TestDecoded', 1)
    androguardClasses = getPermissionsAndClasses('datasets/Test', 10)[1]
    equalSuccessful = 0
    containsSuccessful = 0
    classTypes = ['internal', 'external', 'all']
    for i in range(len(classes)):
        for j in range(len(androguardClasses)):
            if classes[i]['hash'] == androguardClasses[j]['hash']:
                notEqual = True
                notContains = True
                for classType in classTypes: 
                    if classes[i][classType] != androguardClasses[j][classType]:
                        notEqual = False
                    if len(androguardClasses[j][classType] - classes[i][classType]) != 0:
                        notContains = False
                if notEqual:
                    equalSuccessful += 1
                if notContains:
                    containsSuccessful += 1

    print(f"[+] 10 samples tested")
    print(f"[+] {equalSuccessful} classes from samples are correct compared to Androguard") 
    print(f"[+] {containsSuccessful} clasess from samples contains classes from Androguard") 

if __name__ == "__main__":
    testGetPermissions()
    testGetClasses()
