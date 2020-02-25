import logging
from assets.readFileLines import parseIpsFromFile
from assets.saveFileLines import saveLinesToOutput, openOutput
from assets.netProber import getUrlResponses
from assets.whoisExtractor import getIpsAndContacts

logChunks = parseIpsFromFile("IO/inputA.txt")
if(len(logChunks) > 0):
    print()
    print("---   Probing...    ---")
    ips, contacts = getIpsAndContacts(list(logChunks.keys()))
    [logChunks[ip].setContacts(contacts[ip]) for ip in logChunks.keys()]

    saveLinesToOutput(
        sorted(logChunks, key=lambda ip: logChunks[ip].chunkName), "IO/output2.txt")
    openOutput("IO/output2.txt")
else:
    print("No input file found or the file is empty....\nplease create a file"
          " named 'input.txt' and place it in 'IO' folder of this program.")

input("Press Enter to continue...")
