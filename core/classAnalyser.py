import os
import re
import random

def formatClass(item):
    if "}," in item and ";->" in item:
        return item.split("},")[1].split(";")[0].replace(" ", "")
    else:
        return ""

def className(root, smaliFile):
    smaliCode = os.path.join(root, smaliFile)
    with open(smaliCode, "r") as f:
        name = re.findall((r"\.class.*"), f.read())[0]
        name = name.split()
        name = name[len(name)-1][1:-1]
    return name

def returnClasses(root, smaliFile):
    smaliCode = os.path.join(root, smaliFile)
    with open(smaliCode, "r") as f:
        method = re.findall(r"invoke-virtual.*|invoke-super.*|invoke-direct.*|invoke-static.*|invoke-interface.*", f.read())
        if method:
            method = [formatClass(item)[1:] if formatClass(item).startswith("L") else formatClass(item)[2:] for item in method if item != ""]
    return method

def getSmaliFolders(sourceCode):
    return [file for file in sourceCode if re.search(r'smali_classes\d+|smali', file)]

def getClasses(targetDir, limit):
    classesList = []
    decodedSamples = os.listdir(targetDir)
    random.shuffle(decodedSamples)
    i = 0
    for application in decodedSamples[:limit]:
        isApplication = False
        classes = set()
        internalClasses = set() 
        sourceCodePath = os.path.join(targetDir, application)
        sourceCode = os.listdir(sourceCodePath)
        smaliFolders = getSmaliFolders(sourceCode)
        i += 1
        for folders in smaliFolders:
            for root, _, files in os.walk(os.path.join(sourceCodePath, folders)):
                isApplication = True
                for smaliFile in files:
                    if(smaliFile.endswith(".smali")):
                        internalClasses.add(className(root, smaliFile))
                        classes.update(returnClasses(root, smaliFile))
                        classes.discard("")
        if isApplication:
            classInfo = {
                "hash": application,
                "internal": internalClasses, 
                "external": classes - internalClasses,
                "all": classes | internalClasses
            }
            classesList.append(classInfo)
    return classesList
