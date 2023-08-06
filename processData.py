import pickle

classesFrequency = {}

with open("test.pkl", "rb") as f:
    classList = pickle.load(f)

for classes in classList:
    for appClass in classes:
        if appClass not in classesFrequency:
            classesFrequency[appClass] = 1
        else:
            classesFrequency[appClass] += 1

print(dict(sorted(classesFrequency.items(), key=lambda x:x[1])))
