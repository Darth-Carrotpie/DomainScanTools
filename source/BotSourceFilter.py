import logging
from assets.readFileLines import parseIpsFromFiles, countTotalLinesInFiles, getInputFilePaths
from assets.saveFileLines import saveLinesToOutput, openOutput
from assets.netProber import getUrlResponses
from assets.whoisExtractor import getIpsAndContacts
import sys

print("Enter options if needed. Otherwise leave empty. Options available:")
print("-o    :open output files after completion.")
print("-csv    :input files are of type .csv instead of a single input.txt.")
arguments = input("Input:")
# print("-i    :specify input file name other than 'input.txt'.")
# arguments = str(sys.argv)
inputFilePaths = getInputFilePaths("-csv" in arguments, "inputA.txt")
# print([x for x in inputFilePaths])
logChunks = parseIpsFromFiles(inputFilePaths)
if(len(logChunks) > 0):
    print()
    print("---   Probing...    ---")
    ips, contacts = getIpsAndContacts(list(logChunks.keys()))
    [logChunks[ip].setContacts(contacts[ip])
     for ip in logChunks.keys() if ip in contacts]
    print("total log lines: "+str(countTotalLinesInFiles(inputFilePaths)))
    print("total unique ips: "+str(len(logChunks)))
    sortedChunks = sorted(logChunks, key=lambda ip: logChunks[ip].chunkName)
    linesToSave = []
    currentName = ""
    outputFileNames = []
    for ip, chunk in sorted(logChunks.items(), key=lambda kv: (kv[1].chunkName,
                                                               kv[0])):
        newName = chunk.chunkCountry+"_"+chunk.chunkName[:10]
        if currentName != newName:
            if(currentName != ""):
                outputFileNames.append(
                    saveLinesToOutput(linesToSave, currentName))
            # print("oldname: "+currentName + " newname: "+newName)
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
