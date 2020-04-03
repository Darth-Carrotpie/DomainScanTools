
import time
from assets.objects.getUrlThread import GetUrlThread
from .stringRegexHelper import getEmails
from .whoisExtractor import getIpsAndContacts


def getUrlResponses(urls):
    prefixes = ['https://', 'http://']
    start = time.time()
    threads = []
    aliveUrls = []
    for pre in prefixes:
        for url in urls:
            if(pre in url):
                t = GetUrlThread(url)
            else:
                t = GetUrlThread(pre + url)
            threads.append(t)
            t.start()
        for t in threads:
            t.join()
            if(len(t.alive) > 1):
                if(t.alive not in aliveUrls):
                    aliveUrls.append(t.alive)
    print()
    print("--- Probing COMPLETED ---")
    print("Elapsed time: %s" % (time.time() - start))
    urls, contacts = getIpsAndContacts(aliveUrls, False)
    outputLineList = []
    for ip, ip2 in zip(urls, contacts):
        outputLineList.append(str(contacts[ip]).replace('"', "&%").
                              replace("&%'", " ").replace("&%", " "))
        for i in range(len(urls[ip])):
            row = urls[ip][i].replace("http", "hXXp")
            outputLineList.append(row)
        outputLineList.append("\n")

    print("---   URLs Probed:  {}   ---".format(len(aliveUrls)))
    print("---   IPs Found:  {}   ---".format(len(contacts)))
    providers = list(x["name"] for x in contacts.values())
    print("---   Providers Found:  {}   ---".format(len(providers)))
    print("--- ", providers, " ---")
    return outputLineList
