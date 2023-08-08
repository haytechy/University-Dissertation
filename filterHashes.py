import requests
import pickle
from concurrent.futures import ThreadPoolExecutor
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')
VTAPIKEY = config['VirusTotal']['apikey']

def getType(hash):
    url = "https://www.virustotal.com/api/v3/files/"
    response = requests.get(f"{url}{hash}", headers={"accept": "application/json", "x-apikey": VTAPIKEY})
    try:
        sampleType = response.json()['data']['attributes']['type_description']
        extension = response.json()['data']['attributes']['type_extension']
        if sampleType == "Android" and extension == "apk":
            return hash
        else:
            return None
    except:
        return None

def md5List(file):
    with open(f"{file}") as f:
        md5List = [md5.strip("\n") for md5 in f.readlines()[6:]]
    return md5List

def generateApkHashes(md5List, file, limit=10):
    apkHashes = []
    executor = ThreadPoolExecutor(max_workers=10)

    for hash in executor.map(getType,  md5List[:limit]):
        if hash is not None:
            apkHashes.append(hash)

    with open(f"{file}", "wb") as f:
        pickle.dump(apkHashes, f)
