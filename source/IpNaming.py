# changelog: use asyncio to parelilize scanning to speed up for large amounts of ips: https://docs.python.org/3/library/asyncio.html
import logging
from assets.readFileLines import parseIpsFromFiles, countTotalLinesInFiles, getInputFilePaths
from assets.saveFileLines import saveLinesToOutput, openOutput
from assets.netProber import getUrlResponses
from assets.whoisExtractor import getIpsAndContacts
from collections import OrderedDict
import sys
import pandas as pd

#print("Enter options if needed. Otherwise leave empty. Options available:")
#print("-o    :open output files after completion.")
#print("-csv    :input files are of type .csv instead of a single input.txt.")
#print("ip=    :which IP in columns is the source IP (default=1)")

#arguments = input("Input:")
inputFilePaths = getInputFilePaths(True, "input.txt")
#ipNo = [i for i in arguments.split() if "ip=" in i]
#if len(ipNo) > 0:
#    ipNo = int(ipNo[0].replace("ip=", ""))
#else:
#    ipNo = 1
print()
csvs = [pd.read_csv(pt) for pt in inputFilePaths]
print("total files found: "+len(csvs))
dfs = [df.set_index('id') for df in dfList]
print len(pd.concat(dfs, axis=1))

if(len(csvs) > 0):
    print()
    print("---   Probing...    ---")
else:
    print("No input file found or the file is empty....\nplease create a file"
          " named 'input.txt' and place it in 'IO' folder of this program.")

input("Press Enter to continue...")
