# changelog: use asyncio to parelilize scanning to speed up for large amounts of ips: https://docs.python.org/3/library/asyncio.html
# write to files incrementaly?
import logging
from assets.readFileLines import parseIpsFromFiles, countTotalLinesInFiles, getInputFilePaths
from assets.saveFileLines import saveLinesToOutput, openOutput
from assets.netProber import getUrlResponses
from assets.whoisExtractor import getIpsAndContacts
from assets.objects.folderGroupAssembly import FolderGroupAssembly
from collections import OrderedDict
import sys
from collections import Counter
import os

print("Enter options if needed. Otherwise leave empty. Options available:")
print("-o    :open output files after completion.")
print("--no-f    :do NOT folderize output files by email domain instances.")
print("-txt    :input files are by default of type .csv. This will input input.txt instead.")
print("ip=    :which IP in columns is the source IP (default=1)")

arguments = input("Input:")
inputFilePaths = getInputFilePaths("-txt" not in arguments, "input.txt")
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
    [logChunks[ip].setContacts(contacts[ip]) for ip in logChunks.keys() if ip in contacts]
    print("total log lines: "+str(countTotalLinesInFiles(inputFilePaths)))
    print("total unique ips: "+str(len(logChunks)))

    if "--no-f" not in arguments:
        # find unique emails and prepare names for foldering

        allEmails = [item["email"] for item in
                     list(contacts.values())]
        flatEmailsList = [
            item for sublist in allEmails for item in sublist]

        emailsFiltered = [
            item for item in flatEmailsList if not any(x in item for x in ["gmail", "yahoo"])]
        folderGroupAsm = FolderGroupAssembly(ids=emailsFiltered, chunks=list(sortedChunks.values()))
        folderGroupAsm.Group()
        outputFileNames = folderGroupAsm.SaveGroupsToFile()
        print(folderGroupAsm)
        print(str(len(outputFileNames))+" files written")
        #calculate filesizes total:
        totalSize = 0
        for fileNameOpen in outputFileNames:
            totalSize += os.stat(fileNameOpen).st_size
        print("written files size sum: "+str(totalSize/1000)+"kb")
        # open all files that were saved:
        if "-o" in arguments:
            for fileNameOpen in outputFileNames:
                print("opening: "+fileNameOpen)
                openOutput(fileNameOpen)

else:
    print("No input file found or the file is empty....\nplease create a file"
          " named 'input.txt' and place it in 'IO' folder of this program.")

#input("Press Enter to continue...")
