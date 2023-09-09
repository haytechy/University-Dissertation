from androguard.misc import AnalyzeAPK
import os

def analyseAPK(file):
    apkFile, _, dx = AnalyzeAPK(file)
    permissions = [permission for permission in apkFile.get_permissions()]
    classes = [ str(dexClass.name[1:-1]) for dexClass in dx.get_classes()]
    externalClasses = [ str(dexClass.name[1:-1]) for dexClass in dx.get_external_classes()]
    return permissions, classes, externalClasses

def getPermissionsAndClasses(targetDir, limit):
    classesList = []
    permissionsList = []
    decodedSamples = os.listdir(targetDir)
    for application in decodedSamples[:limit]:
        permissions = set()
        classes = set()
        externalClasses = set()
        permissions, apkClass, apkExternalClass = analyseAPK(os.path.join(targetDir, application,))
        classes.update(apkClass)
        externalClasses.update(apkExternalClass)
        classInfo = {
            "hash": application[:-4],
            "internal": classes - externalClasses, 
            "external": externalClasses,
            "all": classes 
        }
        permissionsList.append({"hash": application[:-4], "permissions": set(permissions)})
        classesList.append(classInfo)
    return permissionsList, classesList
