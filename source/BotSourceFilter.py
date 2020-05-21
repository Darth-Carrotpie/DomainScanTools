import logging
from assets.readFileLines import parseIpsFromFiles, countTotalLinesInFiles, getInputFilePaths
from assets.saveFileLines import saveLinesToOutput, openOutput
from assets.netProber import getUrlResponses
from assets.whoisExtractor import getIpsAndContacts
from collections import OrderedDict
import sys

print("Enter options if needed. Otherwise leave empty. Options available:")
print("-o    :open output files after completion.")
print("-csv    :input files are of type .csv instead of a single input.txt.")
print("ip=    :which IP in columns is the source IP (default=1)")

arguments = input("Input:")
inputFilePaths = getInputFilePaths("-csv" in arguments, "input.txt")
ipNo = [i for i in arguments.split() if "ip=" in i]
if len(ipNo) > 0:
    ipNo = int(ipNo[0].replace("ip=", ""))
else:
    ipNo = 1

logChunks = parseIpsFromFiles(inputFilePaths, ipNo)

if(len(logChunks) > 0):
    print()
    print("---   Probing...    ---")
    ips, contacts = getIpsAndContacts(list(logChunks.keys()), True)
    [logChunks[ip].setContacts(contacts[ip])
     for ip in logChunks.keys() if ip in contacts]
    print("total log lines: "+str(countTotalLinesInFiles(inputFilePaths)))
    print("total unique ips: "+str(len(logChunks)))
    # sortedChunks = sorted(
    #    {logChunks[key] for key in logChunks.keys() if logChunks[key].chunkName}, key=lambda ip: logChunks[ip].chunkName)
    sortedChunks = OrderedDict(sorted({item for item in logChunks.items() if ((item[1] is not None) and (item[1].chunkName is not None))},
                                      key=lambda x: (logChunks[x[0]].chunkName, x[0])))
    #sortedChunks = sorted(logChunks, key=lambda ip: logChunks[ip].chunkName)
    linesToSave = []
    currentName = ""
    outputFileNames = []
    # for ip, chunk in sorted(sortedChunks.items(), key=lambda kv: (kv[1].chunkName,
    #                                                              kv[0])):
    for ip, chunk in sortedChunks.items():
        newName = chunk.chunkCountry+"_"+chunk.chunkName[:10]
        if currentName != newName:
            if(currentName != ""):
                outputFileNames.append(
                    saveLinesToOutput(linesToSave, currentName))
            currentName = newName
            linesToSave = []
            linesToSave.append(str(chunk.contacts).replace('"', "&%").
                               replace("&%'", " ").replace("&%", " "))
            linesToSave.append(chunk.titlesLine)
        linesToSave.extend(chunk.mylogs)
    print("total chunks saved: "+str(len(outputFileNames)))
    if(currentName != ""):
        outputFileNames.append(
            saveLinesToOutput(linesToSave, currentName))
    # open all files that were saved:
    if "-o" in arguments:
        for fileNameOpen in outputFileNames:
            print("opening: "+fileNameOpen)
            openOutput(fileNameOpen)
else:
    print("No input file found or the file is empty....\nplease create a file"
          " named 'input.txt' and place it in 'IO' folder of this program.")

input("Press Enter to continue...")
