import os
import re

def formatClass(item):
    return item.split("},")[1].split(";")[0].replace(" ", "")

def returnClasses(root, smaliFile):
    smaliCode = os.path.join(root, smaliFile)
    with open(smaliCode, "r") as f:
        method = re.findall(r"invoke-virtual.*", f.read())
        if method:
            method = [formatClass(item)[1:] if formatClass(item).startswith("L") else formatClass(item)[2:] for item in method]
    return method

def getClasses(targetDir):
    for application in os.listdir(targetDir):
        classes = set()
        sourceCodePath = os.path.join(targetDir, application)
        sourceCode = os.listdir(sourceCodePath)
        if 'smali' in sourceCode:
            for root, _, files in os.walk(os.path.join(sourceCodePath, "smali")):
                for smaliFile in files:
                    if(smaliFile.endswith(".smali")):
                        classes.update(returnClasses(root, smaliFile))
