#!/usr/bin/python3
import logging
from assets.readFileLines import parseUrlsFromFile, getInputFilePaths
from assets.saveFileLines import saveLinesToOutput, openOutput
from assets.netProber import getUrlResponses
urls = parseUrlsFromFile("input.txt")


if(len(urls) > 0):
    print()
    print("---   Probing...    ---")
    responses = getUrlResponses(urls)
    saveLinesToOutput(responses, "scan")
    openOutput("scan")
else:
    print("No input file found or the file is empty....\nplease create a file"
          " named 'input.txt' and place it in 'IO' folder of this program.")

input("Press Enter to continue...")
