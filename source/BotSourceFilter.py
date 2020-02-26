import logging
from assets.readFileLines import parseIpsFromFile, countTotalLinesInFile
from assets.saveFileLines import saveLinesToOutput, openOutput
from assets.netProber import getUrlResponses
from assets.whoisExtractor import getIpsAndContacts
import sys

print("Options:")
print("-o    :open output files after completion.")
# print("-i    :specify input file name other than 'input.txt'.")
arguments = str(sys.argv)
inputFile = "IO/input2.txt"
logChunks = parseIpsFromFile(inputFile)
if(len(logChunks) > 0):
    print()
    print("---   Probing...    ---")
    ips, contacts = getIpsAndContacts(list(logChunks.keys()))
    [logChunks[ip].setContacts(contacts[ip])
     for ip in logChunks.keys() if ip in contacts]
    #print("first log lines: "+str(len(next(iter(logChunks.values())).mylogs)))
    print("total log lines: "+str(countTotalLinesInFile(inputFile)))
    print("total unique ips: "+str(len(logChunks)))
    # print(str(next(iter(logChunks.values()))))
    sortedChunks = sorted(logChunks, key=lambda ip: logChunks[ip].chunkName)
    linesToSave = []
    currentName = ""
    outputFileNames = []
    for ip, chunk in sorted(logChunks.items(), key=lambda kv: (kv[1].chunkName,
                                                               kv[0])):
        newName = chunk.chunkCountry+"_"+chunk.chunkName
        if currentName != newName:
            if(currentName != ""):
                outputFileNames.append(
                    saveLinesToOutput(linesToSave, currentName))
            # print("oldname: "+currentName + " newname: "+newName)
            currentName = newName
            linesToSave = []
            linesToSave.append(chunk.contacts)
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
