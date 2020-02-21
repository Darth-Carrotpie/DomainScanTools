#!/usr/bin/python3
import time
import urllib.request
from threading import Thread
from urllib.error import HTTPError, URLError
import socket
import logging
import os
import re
from ipwhois import IPWhois


class GetUrlThread(Thread):
    def __init__(self, url):
        self.url = url
        super(GetUrlThread, self).__init__()
        self.alive = ""

    def run(self):
        try:
            # .read() .decode('utf-8', 'ignore')
            response = urllib.request.urlopen(self.url, timeout=10)
        except HTTPError as error:
            logging.error(
                'Data not retrieved because %s\nURL: %s', error, self.url)
        except URLError as error:
            if isinstance(error.reason, socket.timeout):
                logging.error('socket timed out - URL %s', self.url)
            else:
                logging.error(
                    'some other error happened while probing: ' + self.url)
        else:
            logging.info('Access successful.')
            print(self.url + "  " + str(response.getcode()))
            self.alive = self.url
        # resp = urllib.request.urlopen(self.url)


def parse_urls():
    filepath = "IO/input.txt"
    urls = []
    if os.path.isfile(filepath):
        print("--- Reading Input File ---")
        with open(filepath) as fp:
           cnt = 0
           for line in fp:
               if(len(line) > 1):
                   link = ""
                   if("//" in line):
                       parts = line.split("//", 1)
                       link = parts[1] if len(parts) > 1 else parts[0]
                       link = link.split(' ')[0].rstrip().replace(
                           "[", '').replace(']', '')
                   else:
                       if(" " in line):
                           link = line.split(' ')[1].rstrip().replace("[", '').replace(']', '')
                   if(len(link) <= 1):
                       link = re.findall(r'[0-9]+(?:\.[0-9]+){3}', line)
                   else:
                       if(len(link) > 1 and link not in urls):
                          urls.append(link)
                          print("Link {}:  -   {}".format(cnt, link))

                   if(cnt % 10 == 0):
                       pass
                       # print()
                   cnt += 1
    return urls


def get_emails(s):
    emailRegex = re.compile(("([a-z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`"
                    "{|}~-]+)*(@|\sat\s)(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?(\.|"
                    "\sdot\s))+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)"))
    return {email[0] for email in re.findall(emailRegex, s) if not email[0].startswith('//')}


def get_contacts(urls):
    ips = {}

    for url in urls:
        try:
            ip = socket.gethostbyname(url.split("//",1)[1].split("/",1)[0])
            if(ip not in ips):
                ips[ip] = [url]
            else:
                if(url not in ips[ip]):
                    ips[ip].append(url)
        except socket.gaierror as error:
             logging.error('could not get IP from socket of URL: '+url.split("//",1)[1].split("/",1)[0])
    contacts = {}
    for ip in ips:
        obj = IPWhois(ip)
        res = obj.lookup_rdap()
        # print(res)
        abuseEntity = res["entities"][len(res["entities"]) - 1]
        # print("abuse Entity: "+abuseEntity)
        abuseObj = res["objects"][abuseEntity]
        providerName = abuseObj["contact"]["name"]

        # abuseEmail = abuseObj["contact"]["email"][len(abuseObj["contact"]["email"])-1]["value"] if abuseObj["contact"]["email"] != None else 'no abuse email found - try manual lookup'
        print(str(res))
        abuseEmail = get_emails(str(res))
        contacts[ip] = {"country":res["asn_country_code"], "name":providerName, "description":res["asn_description"], "ip":ip, "email":abuseEmail}
    # print(contacts)
    return ips, contacts


def save_urls(urls):
    # print("trying to save...:")
    # print(urls)
    with open("IO/output.txt", 'w') as output:
        for row in urls:
            output.write(str(row) + '\n')


def get_responses(urls):
    prefixes = ['https://', 'http://']
    start = time.time()
    threads = []
    aliveUrls = []
    for pre in prefixes:
        for url in urls:
            if(pre in url):
                t = GetUrlThread(url)
            else:
                t = GetUrlThread(pre+url)
            threads.append(t)
            t.start()
        for t in threads:
            t.join()
            if(len(t.alive) > 1):
                if(t.alive not in aliveUrls):
                    aliveUrls.append(t.alive)
    print()
    # print(aliveUrls)
    print("--- Probing COMPLETED ---")
    print("Elapsed time: %s" % (time.time()-start))
    # save_urls(aliveUrls)
    urls, contacts = get_contacts(aliveUrls)
    outputLineList = [] # contacts[i] if i % 2 == 0 else urls[i] for line in range(len(urls) + len(contacts))
    for ip, ip2 in zip(urls, contacts):
        outputLineList.append(contacts[ip])
        for i in range(len(urls[ip])):
            row = urls[ip][i].replace("http", "hXXp")
            outputLineList.append(row)
        outputLineList.append("\n")
    save_urls(outputLineList)
    print("---   URLs Probed:  {}   ---".format(len(aliveUrls)))
    print("---   IPs Found:  {}   ---".format(len(contacts)))
    providers = list(x["name"] for x in contacts.values())
    print("---   Providers Found:  {}   ---".format( len(providers)))
    print("--- ",providers, " ---")


urls = parse_urls()
if(len(urls) > 0):
    print()
    print("---   Probing...    ---")
    get_responses(urls)
else:
    print("No input file found or the file is empty....\nplease create a file named 'input.txt' and place it in 'IO' folder of this program.")

input("Press Enter to continue...")
