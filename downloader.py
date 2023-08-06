import requests
import re
import json
import pyzipper
import argparse
import os
import sys

from classAnalyser import getClasses 

APIKEY = "3add204aa97a30fdfaadb86b1a4b7733b8311f1ca9d3468ea9d4619eb5815d37"
MBURL = "https://mb-api.abuse.ch/api/v1"

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
    os.mkdir(dir)
    query = {"query": "get_file", "sha256_hash": hash}
    response = requests.post(MBURL, data=query, timeout=15, allow_redirects=True)
    open(f"{dir}/{hash}.zip", "wb").write(response.content)

def getMalwareByFamily(families):
    hashes = []
    for family in families:
        query = {"query": "get_siginfo", "signature": family, "limit": 1}
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

def getReport(targetdir, outputfile):
    url = "https://www.virustotal.com/api/v3/files/"
    for _, _, files in os.walk(targetdir):
        for sample in files:
            if sample.endswith(".apk") or sample.endswith(".zip"):
                hash = sample[:-4]
                response = requests.get(f"{url}{hash}", headers={"x-apikey": APIKEY})
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

def getPermissions(dataset):
    permissiondict = {}
    total = 0

    for apk in os.listdir(dataset):
        manifest = f"{dataset}/{apk}/AndroidManifest.xml"
        if os.path.isfile(manifest):
            total += 1
            with open(manifest) as f:
                permissions = list(set(re.findall(r"\bandroid\.permission\.[A-Z_]*\b", f.read())))
                for permission in permissions:
                    permission= permission.split('.')[2]
                    if permission in permissiondict:
                        permissiondict[permission] += 1
                    else:
                        permissiondict[permission] = 1
    return dict(sorted(permissiondict.items(), key=lambda x:x[1], reverse=True))



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Dataset Generator")
    subparsers = parser.add_subparsers(title="subcommand", dest="subcommand", description="subcommand")
    
    downloadParser = subparsers.add_parser("download", help="download")
    downloadParser.add_argument('outputfolder', type=str, help="Output Folder")
    downloadParser.add_argument('-m', help="Download Type", dest="mode")

    extractParser = subparsers.add_parser("extract", help="Extract folder containg samples")
    extractParser.add_argument('targetfolder', type=str, help="Target Folder")
    extractParser.add_argument('-o', help="Output Folder", dest="outputfolder")

    reportParser = subparsers.add_parser("report", help="Get VirustTotal report")
    reportParser.add_argument('targetfolder', type=str, help="Target Folder")
    reportParser.add_argument('-o', help="Output File", dest="outputfile")

    permissionParser = subparsers.add_parser("permission", help="Get Permissions based off decompile dataset")
    permissionParser.add_argument('targetdataset', type=str, help="Target Dataset")
    permissionParser.add_argument('-o', help="Output File", dest="outputfile")

    decompileParser = subparsers.add_parser("decompile", help="Extract folder containg samples")
    decompileParser.add_argument('targetfolder', type=str, help="Target Folder")
    decompileParser.add_argument('-o', help="Output Folder", dest="outputfolder")

    classesParser = subparsers.add_parser("classes", help="Extract folder containg samples")
    classesParser.add_argument('targetfolder', type=str, help="Target Folder")

    if len(sys.argv)==1:
        parser.print_help()
        parser.exit()

    args = parser.parse_args()
    if args.subcommand == "download":
        hashes = []
        if args.mode == "family":
            hashes = getMalwareByFamily(["Cerberus", "Hydra", "FluBot", "Octo", "Ermac"])
        if args.mode == "recent":
            hashes = getRecentMalware(1000)
            print(len(hashes))
        outputdir = args.outputfolder
        if not os.path.exists(outputdir):
            for hash in hashes:
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

    
    if args.subcommand == "report":
        outputfile = args.outputfile
        if outputfile is not None:
            if not os.path.exists(outputfile):
                getReport(args.targetfolder, outputfile)
            else:
                print("Directory Exists")

    if args.subcommand == "permission":
        permissions = getPermissions(args.targetdataset)
        if permissions:
            outputfile = args.outputfile
            if outputfile is not None:
                with open(args.outputfile, "w") as f:
                    f.write(json.dumps(permissions))
        else:
            print("Invalid Sample")

    if args.subcommand == "decompile":
        outputdir = args.outputfolder
        if outputdir is not None:
            if not os.path.exists(outputdir):
                decompile(args.targetfolder, outputdir, "dependencies/apktool_2.8.1.jar")
            else:
                print("Directory Exists")

    if args.subcommand == "classes":
        getClasses(args.targetfolder)
