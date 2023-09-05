import requests
import re
import json
import pyzipper
import argparse
import os
import sys
import time
import random
from configparser import ConfigParser

from core.classAnalyser import getClasses 
from core.filterHashes import generateApkHashes
from core.dataProcess import readData, writeData
from graphAnalyser import processPermissions, processClasses

config = ConfigParser()
config.read('config.ini')
VTAPIKEY = config['VirusTotal']['apikey']
VSAPIKEY = config['VirusShare']['apikey']
MBURL = config['MalwareBazaar']['url']

def getHash(query):
    response = requests.post(MBURL, data=query)
    data = response.json()["data"]
    hashes = []
    for i in range(len(data)):
        sample = data[i]
        if sample["file_type"] == "apk":
            hashes.append(sample["sha256_hash"])
    return hashes

def downloadSample(dir, hash):
    query = {"query": "get_file", "sha256_hash": hash}
    response = requests.post(MBURL, data=query, timeout=60, allow_redirects=True)
    open(f"{dir}/{hash}.zip", "wb").write(response.content)

def downloadSampleVS(dir, hash):
    time.sleep(15)
    url = f"https://virusshare.com/apiv2/download?apikey={VSAPIKEY}&hash={hash}"
    response = requests.get(url)
    open(f"{dir}/{hash}.zip", "wb").write(response.content)

def getMalwareByFamily(families, limit):
    hashes = []
    for family in families:
        query = {"query": "get_siginfo", "signature": family, "limit": limit}
        hashes.extend(getHash(query))
    return hashes

def getRecentMalware(limit):
    query = {"query": "get_file_type", "file_type": "apk", "limit": limit}
    return getHash(query)

def extract(targetdir, outputdir):
    os.mkdir(outputdir)
    for archive in os.listdir(targetdir):
        if archive.endswith(".zip"):
            with pyzipper.AESZipFile(f"{targetdir}/{archive}") as zf:
                zf.extractall(path=outputdir, pwd=bytes("infected", "utf-8"))
    for file in os.listdir(outputdir):
        if not file.endswith(".apk"):
            os.rename(f"{outputdir}/{file}", f"{outputdir}/{file}")


def getReport(targetdir, outputfile):
    url = "https://www.virustotal.com/api/v3/files/"
    for _, _, files in os.walk(targetdir):
        for sample in files:
            if sample.endswith(".apk") or sample.endswith(".zip"):
                hash = sample[:-4]
                response = requests.get(f"{url}{hash}", headers={"accept": "application/json", "x-apikey": VTAPIKEY})
                with open(outputfile, "a") as f:
                    json.dump(response.json(), f, ensure_ascii=False)
                    f.write("\n")

def decompile(targetdir, outputdir, apktool):
    samples = []
    for root, _, files in os.walk(targetdir):
        for file in files:
            samples.append(os.path.abspath(os.path.join(root, file)))
    os.mkdir(outputdir)
    apktool = os.path.abspath(apktool)
    for sample in samples:
        if sample.endswith(".apk"):
            os.system(f"cd {outputdir} && java -jar {apktool} d {sample}")

def cleanDecodedSamples(targetdir):
    sampleCount = 0
    fileCount = 0
    for decodedSample in os.listdir(targetdir):
        fileCount += 1
        decodedSample = os.path.join(targetdir, decodedSample)
        if not os.listdir(decodedSample):
            os.rmdir(decodedSample)
        else:
            sampleCount += 1
    print(f"[+] {fileCount} Files processed")
    print(f"[+] {sampleCount} Files successfully decompiled") 
    print(f"[-] {fileCount - sampleCount} Invalid decompiled files removed") 

def getPermissions(targetDir, limit):
    permissionsList = []
    dataset = os.listdir(targetDir) 
    random.shuffle(dataset)
    for sourceCode in dataset[:limit]:
        permissions = []
        manifest = f"{targetDir}/{sourceCode}/AndroidManifest.xml"
        if os.path.isfile(manifest):
            with open(manifest) as f:
                permissions = re.findall(r'<uses-permission.*?\/>', f.read()) #Regex to extraction permissions from AnroidManifest
                permissions = [re.search(r'"(.*?)"', permission).group()[1:-1] for permission in permissions if re.search(r'"(.*?)"', permission)]
        permissionsList.append({"hash": sourceCode, "permissions": set(permissions)})
    return permissionsList


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Dataset Generator", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    subparsers = parser.add_subparsers(title="subcommand", dest="subcommand", description="subcommand")
    
    downloadParser = subparsers.add_parser("download", help="Download Recent Malware samples from Virus Sample hosting platforms")
    downloadParser.add_argument('outputfolder', type=str, help="Output Folder")
    downloadParser.add_argument('-m', choices=['MalwareBazaarRecent', 'MalwareBazaarFamily', 'VirusShareRecent'], help="Download Type", dest="mode")
    downloadParser.add_argument('-s', default=100, type=int, help="Number of Samples to Download", dest="size")

    extractParser = subparsers.add_parser("extract", help="Extract folder containg zipped samples")
    extractParser.add_argument('targetfolder', type=str, help="Target Folder")
    extractParser.add_argument('-o', help="Output Folder", dest="outputfolder")

    decompileParser = subparsers.add_parser("decompile", help="Decompile folder containg APK samples")
    decompileParser.add_argument('targetfolder', type=str, help="Target Folder")
    decompileParser.add_argument('-o', help="Output Folder", dest="outputfolder")

    filterParser = subparsers.add_parser("filter", help="Filter a list of MD5 from VirusShare for APK files")
    filterParser.add_argument('targetfile', type=str, help="VirusShare MD5 File")

    permissionParser = subparsers.add_parser("permissions", help="Get Permissions based off decompiled datasets")
    permissionParser.add_argument('targetfolder', type=str, help="Target Decoded Sample Folder")
    permissionParser.add_argument('-s', default=10, type=int, help="Number of Samples to get Permissions", dest="size")

    classesParser = subparsers.add_parser("classes", help="Extracts classes from decompiled datasets")
    classesParser.add_argument('targetfolder', type=str, help="Target Decoded Sample Folder")
    classesParser.add_argument('-s', default=10, type=int, help="Number of Samples to get Classes", dest="size")

    graphParser = subparsers.add_parser("graph", help="Produce Graphs from two datasets")
    graphParser.add_argument('targetdata', type=str, help="Target Data")
    graphParser.add_argument('-t', help="Type of Feature", dest="type")
    graphParser.add_argument('-d', help="Comparison Data", dest="comparedata")
    graphParser.add_argument('-s', default=100, type=int, help="Number of Samples Retrieve in each Dataset", dest="size")
    graphParser.add_argument('-c', default=20, type=int, help="Number of Categories to Display", dest="categorySize")

    if len(sys.argv)==1:
        parser.print_help()
        parser.exit()
    args = parser.parse_args()

    if args.subcommand == "download":
        hashes = []
        if args.mode == "MalwareBazaarFamily":
            hashes = getMalwareByFamily(["Cerberus", "Hydra", "FluBot", "Octo", "Ermac"], args.size)
        if args.mode == "MalwareBazaarRecent":
            hashes = getRecentMalware(args.size)
        if args.mode == "VirusShareRecent":
            data = readData("data/VirusShare/VirusShare_00476.pkl")
            if data:
                hashes = data['hashes'][:args.size]
        else:
            print("No mode specified")
        outputdir = args.outputfolder
        if not os.path.exists(outputdir):
            os.mkdir(outputdir)
            if hashes:
                for hash in hashes:
                    if args.mode == "VirusShareRecent":
                        downloadSampleVS(outputdir, hash)
                    else:
                        downloadSample(outputdir, hash)
        else:
            print("Directory Exists")

    if args.subcommand == "extract":
        outputdir = args.outputfolder
        if args.outputfolder is not None:
            if not os.path.exists(outputdir):
                extract(args.targetfolder, outputdir)
            else:
                print("Directory Exists")
        else:
            print("Output Folder Required (-o)")
    

    if args.subcommand == "decompile":
        outputdir = args.outputfolder
        if outputdir is not None:
            if not os.path.exists(outputdir):
                decompile(args.targetfolder, outputdir, "dependencies/apktool_2.8.1.jar")
                cleanDecodedSamples(outputdir)
            else:
                print("Directory Exists")
        else:
            print("Required Output Folder")

    if args.subcommand == "filter":
        md5File = args.targetfile 
        if os.path.exists(md5File):
            outputFileName = os.path.basename(md5File)[:-4]
            fileHashes = readData(f"data/VirusShare/{outputFileName}.pkl") # Get saved hashes
            if fileHashes:
                apkHashes, count = generateApkHashes(md5File, fileHashes['hashes'], fileHashes['count'])
            else:
                apkHashes, count = generateApkHashes(md5File, [], 0)
            if apkHashes and count:
                writeData({"hashes": apkHashes, "count": count}, "VirusShare", outputFileName)

    if args.subcommand == "permissions":
        targetdir = args.targetfolder
        dirName = os.path.basename(targetdir)
        if dirName == "":
            dirName = os.path.basename(os.path.dirname(targetdir))
        permissions = getPermissions(targetdir, args.size)
        if permissions:
            writeData(permissions, dirName, "permissions")
        else:
            print("Invalid Sample")

    if args.subcommand == "classes":
        targetdir = args.targetfolder
        dirName = os.path.basename(targetdir)
        if dirName == "":
            dirName = os.path.basename(os.path.dirname(targetdir))
        classes = getClasses(targetdir, args.size)
        if classes:
            writeData(classes, dirName, "classes")
        else:
            print("Invalid Sample")

    if args.subcommand == "graph":
        targetdata = args.targetdata
        comparedata = args.comparedata
        sampleSize = args.size
        categorySize = args.categorySize
        if args.type == "permissions":
            processPermissions(f"{targetdata}/permissions.pkl", f"{comparedata}/permissions.pkl", categorySize, sampleSize)
        elif args.type == "classes":
            processClasses(f"{targetdata}/classes.pkl", f"{comparedata}/classes.pkl", categorySize, sampleSize)
        else:
            print("No type specified")
