import requests
import os
from concurrent.futures import ThreadPoolExecutor
from configparser import ConfigParser

config = ConfigParser()
config.read(os.path.abspath('config.ini'))
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

def listmd5(file):
    with open(f"{file}") as f:
        md5List = [md5.strip("\n") for md5 in f.readlines()[6:]]
    return md5List

def generateApkHashes(md5File, apkHashes):
    if apkHashes:
        md5List = listmd5(md5File)
        executor = ThreadPoolExecutor(max_workers=5)

        for hash in executor.map(getType,  md5List[36000:50000]):
            if hash is not None:
                apkHashes.append(hash)
    return apkHashes

