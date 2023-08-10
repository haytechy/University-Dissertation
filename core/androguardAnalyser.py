import random
from timeit import default_timer as timer
from androguard.core.bytecodes import apk, dvm
import androguard.core.analysis.analysis as analysis
import os

def analyseAPK(file):
    apkFile = apk.APK(file)
    dalvik = dvm.DalvikVMFormat(apkFile)
    dx = analysis.Analysis(dalvik)
    permissions = [permission.split(".")[2] for permission in apkFile.get_permissions()]
    classes = [ dexClass.name[1:-1] for dexClass in list(dx.get_classes())]
    externalClasses = [ dexClass.name[1:-1] for dexClass in list(dx.get_classes()) if dexClass.is_external()]
    return permissions, classes, externalClasses

def getPermissionsAndClasses(targetDir, limit):
    classesList = []
    permissionsList = []
    decodedSamples = os.listdir(targetDir)
    random.shuffle(decodedSamples)
    limit = limit if limit < len(decodedSamples) else len(decodedSamples)
    for application in decodedSamples[:limit]:
        classes = set()
        externalClasses = set()
        permissions, apkClass, apkExternalClass = analyseAPK(os.path.join(targetDir, application,))
        classes.update(apkClass)
        externalClasses.update(apkExternalClass)
        classInfo = {
            "hash": application,
            "internal": classes - externalClasses, 
            "external": externalClasses,
            "all": classes 
        }
        permissionsList.append({"hash": application, "permissions": set(permissions)})
        classesList.append(classInfo)
    return permissionsList, classesList
