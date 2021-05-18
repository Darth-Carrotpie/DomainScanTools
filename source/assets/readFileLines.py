import os
from .stringRegexHelper import getIPFromLine
from .objects.LogChunk import LogChunk
from .objects.IPGroup import IPGroup
import __main__ as main
from os import path
import csv
import re


def parseUrlsFromFile(fileName):
    urls = []
    currPath = path.dirname(path.abspath(main.__file__))
    absPath = path.join(currPath, "IO")
    fullPath = path.join(absPath, fileName)
    if os.path.isfile(fullPath):
        print("--- Reading Input File ---")
        with open(fullPath) as fp:
            cnt = 0
            for line in fp:
                if(len(line) > 1):
                    link = ""
                    if("//" in line):
                        parts = line.split("//", 1)
                        link = parts[1] if len(parts) > 1 else parts[0]
                        link = link.split(' ')[0].rstrip().replace(
                            "[", '').replace(']', '')
                    else:
                        if(" " in line):
                            link = line.split(' ')[1].rstrip().replace(
                                "[", '').replace(']', '')
                    if(len(link) <= 1):
                        link = re.findall(r'[0-9]+(?:\.[0-9]+){3}', line)
                    else:
                        if(len(link) > 1 and link not in urls):
                            urls.append(link)
                            print("Link {}:  -   {}".format(cnt, link))

                    if(cnt % 10 == 0):
                        pass
                    cnt += 1
    return urls


def parseIpsFromFiles(filepaths, ipNo):
    chunks = {}
    titlesLine = ""
    for filepath in filepaths:
        print("checking filepath: "+filepath)
        if path.isfile(filepath):
            print("--- Reading Input File ---")
            with open(filepath, newline='') as fp:
                if(filepaths[0].endswith(".csv")):
                    fp = csv.reader(fp)
                for line in fp:
                    line = ','.join(line)
                    print(line)
                    # print(len(line))
                    if(len(line) > 1):
                        newIP = getIPFromLine(line, ipNo)
                        if(newIP):
                            if newIP in chunks:
                                chunks[newIP].addChunkLine(line)
                            else:
                                chunks[newIP] = LogChunk(newIP)
                                chunks[newIP].setTitlesLine(titlesLine)
                                chunks[newIP].addChunkLine(line)
                        else:
                            titlesLine = line
    print("--- Read {} Unique IPs ---".format(len(chunks)))
    return chunks

def countTotalLinesInFiles(files):
    def blocks(files, size=65536):
        while True:
            b = files.read(size)
            if not b:
                break
            yield b

    def openAndRead(file):
        with open(file, "r", encoding="utf-8", errors='ignore') as f:
            return(sum(bl.count("\n") for bl in blocks(f)))

    return sum(list(map(openAndRead, files)))


def getInputFilePaths(isCsv, defaultName):
    curr_path = path.dirname(path.abspath(main.__file__))
    abs_path = path.join(curr_path, "IO")
    outputPaths = []
    if not isCsv:
        outputPaths.append(path.join(abs_path,  defaultName))
    else:
        for root, dirs, files in os.walk(abs_path):
            for file in files:
                if file.endswith(".csv"):
                    outputPaths.append(os.path.join(root, file))

    return outputPaths
