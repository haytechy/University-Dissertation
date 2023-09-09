import matplotlib.pyplot as plt
from collections import Counter
from core.dataProcess import readData, getClassesFrequency, getPermissionsFrequncy, getSampleSize, validateAPI
import os
import numpy as np

def formatData(data, categories):
    data = data.most_common(categories)
    return [item[0] for item in data], [item[1] for item in data]

def processSample(file1, file2, size=None):
    dataset = os.path.basename(os.path.dirname(file1))
    dataset2 = os.path.basename(os.path.dirname(file2))
    sampleSize = getSampleSize(file1)
    sampleSize2 = getSampleSize(file2)
    if size is None or size > sampleSize or size > sampleSize2:
        size = sampleSize if sampleSize < sampleSize2 else sampleSize2
    return dataset, dataset2, size


def processGraphData(category, featureType, categorySize, sampleSize, frequency, frequency2, dataset, dataset2):
    category = category[::-1]
    frequency = frequency[::-1]
    frequency2 = frequency2[::-1]
    y = np.arange(len(category))
    barWidth = 0.3
    dataset = dataset.replace("Decoded", "")
    dataset2 = dataset2.replace("Decoded", "")
    plt.barh(y - barWidth/2, frequency, barWidth, label=f"{dataset}")
    plt.barh(y + barWidth/2, frequency2, barWidth, label=f"{dataset2}")

    plt.xlabel('Frequency')
    plt.ylabel(f'{featureType}')
    plt.title(f'Top {categorySize} {featureType} from {dataset} Dataset Compared to {dataset2} Dataset ({sampleSize} samples)')
    plt.yticks(y, category)
    plt.legend()

    plt.show()

def processPermissions(file1, file2, categorySize, sampleSize=None):
    dataset, dataset2, size = processSample(file1, file2, sampleSize)
    Data = getPermissionsFrequncy(file1, size)
    Data2 = getPermissionsFrequncy(file2, size)
    category, frequency = formatData(Data, categorySize)
    frequency2 = []
    for permission in category:
        frequency2.append(Data2[permission])
    print(frequency2)
    category = [permission.split(".")[-1] if ".".join(permission.split(".")[0:2]) == "android.permission" else permission for permission in category ]
    processGraphData(category, "Permissions", categorySize, size, frequency, frequency2, dataset, dataset2) 

def processClasses(file1, file2, categorySize, sampleSize=None):
    dataset, dataset2, size = processSample(file1, file2,  sampleSize)
    classTypes = ['internal', 'external', 'all', "Android API", "Non Android API"]
    androidAPI = readData('data/AndroidAPI.pkl')
    categoryList = []
    frequencyList = []
    frequencyList2 = []
    Data = getClassesFrequency(file1, size)
    Data2 = getClassesFrequency(file2, size)
    for types in classTypes: 
        frequency2 = []
        if types == "Android API" or types == "Non Android API":
            if types == "Android API":
                types = 'all'
                filteredData = {key: count for key, count in Data[types].items() if validateAPI(key, androidAPI)}
            else:
                types = 'all'
                filteredData = {key: count for key, count in Data[types].items() if not validateAPI(key, androidAPI)}
            category, frequency = formatData(Counter(filteredData), categorySize)
        else:
            category, frequency = formatData(Data[types], categorySize)
        categoryList.append(category)
        frequencyList.append(frequency)
        for classes in category:
            frequency2.append(Data2[types][classes])
        frequencyList2.append(frequency2)
    for i in range(5):
            category = categoryList[i]
            frequency = frequencyList[i]
            frequency2 = frequencyList2[i]
            processGraphData(category, f"{classTypes[i].capitalize()} Classes", categorySize, size, frequency, frequency2, dataset, dataset2) 
