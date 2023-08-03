import requests
import os

MBURL = "https://mb-api.abuse.ch/api/v1"
VSURL = ""
TARGETDIR = "samples"

def getSignature(signature):
    query = {"query": "get_siginfo", "signature": signature, "limit": 10}
    response = requests.post(MBURL, data=query)
    data = response.json()["data"]
    hashes = []
    for i in range(len(data)):
        sample = data[i]
        if sample["file_type"] == "apk":
            hashes.append(sample["sha256_hash"])
    return hashes

def downloadSample(hash):
    query = {"query": "get_file", "sha256_hash": hash}
    response = requests.post(MBURL, data=query, timeout=15, allow_redirects=True)
    open("samples/{}.zip".format(hash), "wb").write(response.content)

if __name__ == "__main__":
    if not os.path.exists(TARGETDIR):
        os.makedirs(TARGETDIR)
    malwareFamilies = ["Cerberus", "Hydra", "FluBot", "Octo", "Ermac"]
    totalHashes = []
    for i in range(len(malwareFamilies)):
        totalHashes.extend(getSignature(malwareFamilies[i]))
    print(totalHashes)