import pickle
from timeit import default_timer as timer
from androguard.core.bytecodes import apk, dvm
import androguard.core.analysis.analysis as analysis

def loadFile(dataFile):
    with open(dataFile, "rb") as f:
        data = pickle.load(f)
    return data

apkFile = apk.APK("0f218c3d1d72f467b627d3a77f4283b99a35684f0e399cec03742a234e952505.apk")
dalvik = dvm.DalvikVMFormat(apkFile)
dx = analysis.Analysis(dalvik)

classes = [ dexClass.name[1:-1] for dexClass in list(dx.get_classes())]
externalClasses = [ dexClass for dexClass in list(dx.get_classes()) if dexClass.is_external()]
apiClasses = [ dexClass for dexClass in list(dx.get_classes()) if dexClass.is_android_api()]

permissions = loadFile("data/testPermissions.pkl")[0]["permissions"]
print(set(apkFile.get_permissions()) - permissions)
print( permissions - set(apkFile.get_permissions()))
