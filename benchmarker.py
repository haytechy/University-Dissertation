from core.androguardAnalyser import getPermissionsAndClasses
from core.classAnalyser import getClasses
from core.dataProcess import readData, writeData
from droidloader import getPermissions, decompile, cleanDecodedSamples
import timeit
import random
import os
import shutil

def generateSample(targetDir, size, datasets=['datasets/MalwareBazaarRecent', 'datasets/CICAndMal2017']):
    samples = []
    for dataset in datasets:
        datasetSamples = []
        for root, _, files in os.walk(dataset):
            for sample in files:
                datasetSamples.append(os.path.join(root, sample))
        samples.append(datasetSamples)
    samples = random.sample(samples[0], size //2) + random.sample(samples[1], size//2)
    for sample in samples:
        shutil.copy(sample, targetDir)

def decompileTime(sampleDir, targetDir):
    if os.path.exists(targetDir):
        shutil.rmtree(targetDir)
    decompile(sampleDir, targetDir, 'dependencies/apktool_2.8.1.jar')
    cleanDecodedSamples(targetDir)

def permissionsAndClassesTime(sampleDir, size):
    permissions = getPermissions(sampleDir, size)
    classes = getClasses(sampleDir, size)
    return permissions, classes

def permissionsAndClassesAndroguardTime(sampleDir, size):
    permissions, classes = getPermissionsAndClasses(sampleDir, size)
    return permissions, classes

if __name__ == "__main__":
    sampleSize = [10, 25, 50, 100]
    times = readData('data/Benchmark/times.pkl')
    sampleDir = 'datasets/Benchmark'
    decodedDir = 'datasets/BenchmarkDecoded'
    for size in sampleSize:
        if os.path.exists(sampleDir):
            shutil.rmtree(sampleDir)
        os.mkdir(sampleDir)
        generateSample(sampleDir, size)
        execTimeDecompile = timeit.timeit(lambda: decompileTime(sampleDir, decodedDir), number=1)
        execTime = timeit.timeit(lambda: permissionsAndClassesTime(decodedDir, size), number=1)
        execTimeAndroguard = timeit.timeit(lambda: permissionsAndClassesAndroguardTime(sampleDir, size), number=1)
        times.append({"sampleSize": size, "decompileTime": execTimeDecompile, "droidloader": execTime, "androguard": execTimeAndroguard})
        writeData(times, "Benchmark", "times")

