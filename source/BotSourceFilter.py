# changelog: use asyncio to parelilize scanning to speed up for large amounts of ips: https://docs.python.org/3/library/asyncio.html
# write to files incrementaly?
import logging
from assets.readFileLines import parseIpsFromFiles, countTotalLinesInFiles, getInputFilePaths
from assets.saveFileLines import saveLinesToOutput, openOutput
from assets.netProber import getUrlResponses
from assets.whoisExtractor import getIpsAndContacts
from collections import OrderedDict
import sys
from collections import Counter

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
    [logChunks[ip].setContacts(contacts[ip])
     for ip in logChunks.keys() if ip in contacts]
    print("total log lines: "+str(countTotalLinesInFiles(inputFilePaths)))
    print("total unique ips: "+str(len(logChunks)))
    # sortedChunks = sorted(
    #    {logChunks[key] for key in logChunks.keys() if logChunks[key].chunkName}, key=lambda ip: logChunks[ip].chunkName)
    sortedChunks = OrderedDict(sorted({item for item in logChunks.items() if ((item[1] is not None) and (item[1].chunkName is not None))},
                                      key=lambda x: (logChunks[x[0]].chunkName, x[0])))
    # sortedChunks = sorted(logChunks, key=lambda ip: logChunks[ip].chunkName)

    if "--no-f" not in arguments:
        # find unique emails and prepare names for foldering
        allEmails = [item["email"] for item in
                     list(contacts.values())]
        flatEmailsList = [
            item for sublist in allEmails for item in sublist]

        emailsFiltered = [
            item for item in flatEmailsList if not any(x in item for x in ["gmail", "yahoo"])]

        emailInstances = Counter(emailsFiltered)
        emailInstances = {x: count for x,
                          count in emailInstances.items() if count >= 2}

        emailDomains = [x.split("@")[-1] for x in emailInstances.keys()]
        emailDomains = set(emailDomains)
        print(":")
        print("emailDomains:")
        print(emailDomains)
        emailInstances = [e for e in emailInstances.keys() if any(
            x in e for x in emailDomains)]
        print(":")
        print("emailInstances:")
        print(emailInstances)
        folderNames = {email: email.split("@")[-1].replace(".", "_")
                       for email in list(emailInstances)}
        print(":")
        print("folderNames:")
        print(folderNames)
        for ip, chunk in sortedChunks.items():
            chunkEmails = list(chunk.contacts["email"])
            for x in chunkEmails:
                if x in folderNames.keys():
                    chunk.targetFolder = folderNames[x]
                    break

    linesToSave = []
    currentName = ""
    outputFileNames = []
    currentFolder = ""
    # for ip, chunk in sorted(sortedChunks.items(), key=lambda kv: (kv[1].chunkName,
    #                                                              kv[0])):
    for ip, chunk in sortedChunks.items():
        newName = chunk.chunkCountry+"_"+chunk.chunkName[:15]
        if currentName != newName:
            if(currentName != ""):
                outputFileNames.append(
                    saveLinesToOutput(linesToSave, currentName, currentFolder))
            currentName = newName
            currentFolder = chunk.targetFolder
            linesToSave = []
            linesToSave.append(str(chunk.contacts).replace('"', "&%").
                               replace("&%'", " ").replace("&%", " "))
            linesToSave.append(chunk.titlesLine)
        linesToSave.extend(chunk.mylogs)
    print("total files saved: "+str(len(outputFileNames)))

    if(currentName != ""):
        outputFileNames.append(
            saveLinesToOutput(linesToSave, currentName, currentFolder))
    # open all files that were saved:
    if "-o" in arguments:
        for fileNameOpen in outputFileNames:
            print("opening: "+fileNameOpen)
            openOutput(fileNameOpen)
else:
    print("No input file found or the file is empty....\nplease create a file"
          " named 'input.txt' and place it in 'IO' folder of this program.")

input("Press Enter to continue...")
