## When to use
Use this tool when you need to parse data from multiple botnet report feeds or scan phishing site lists for 'alive-worthy' responses. It will output IPs grouped in lists by ASN, appending available contacts to the top.


## Setup
1. Install python if you do not already have it in your system. Tested with versions: **3.8.1**, ...
2. Install by cloning this repo; (```git clone```)
3. Install dependencies from /requirements.txt; (```pip install -r requirements.txt```)


## How to use
1. Put all of the .csv report files into a folder ```/source/IO```. Names and extentions don't matter for .csv type, but for .txt must be called 'input.txt'. Other txts will be ignored;
2. Run a main script:
      - for botnet parsing run /BotSourceFilter.py
      - for phishing activity checkup run /IsPhishingAlive.py
3. Select file type by typing "-csv" into terminal input if the files are csv. If input left empty, type to read will be .txt by default.
4. Your output will be stored as .txt files inside the ```/source/IO``` folder, each named by ASN name.
5. Output is grouped into folders by ASN abuse emails and log chunk size.

## What not to do
1. IO folder is scanned for ALL .csv, if you pick csv format. So delete the unused one before new scans. Otherwise new lists will include all of the logs.
2. Approximate maximum per single scan would theoretically be around **100k log lines**. But not tested yet. If higher than that amount, might get IP banned from the whois service.


## To Do
- parallelize whois rdap requests using asyncio