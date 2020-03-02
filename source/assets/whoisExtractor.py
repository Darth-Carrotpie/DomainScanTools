from ipwhois import IPWhois, HTTPLookupError
from assets.stringRegexHelper import getFirstIP, getEmails
import socket
import logging


def getIpsAndContacts(urls, isIP):
    ips = {}

    for url in urls:
        try:
            if(isIP):
                ip = url
                print("got ip: "+ip)
            else:
                ip = socket.gethostbyname(
                    url.split("//", 1)[1].split("/", 1)[0])
            if(ip not in ips):
                ips[ip] = [url]
            else:
                if(url not in ips[ip]):
                    ips[ip].append(url)
        except socket.gaierror as error:
            logging.error('could not get IP from socket of URL: ',
                          url.split("//", 1)[1].split("/", 1)[0])
    contacts = {}
    for ip in ips:
        if(len(ip) > 7):
            print("looking up: "+ip)
            obj = IPWhois(ip)
            try:
                res = obj.lookup_rdap()
                # print(res)
                abuseEntity, abuseObj, providerName = ("",) * 3
                if(len(res["entities"]) > 0):
                    abuseEntity = res["entities"][len(res["entities"]) - 1]
                    # print("abuse Entity: "+abuseEntity)
                    abuseObj = res["objects"][abuseEntity]
                    providerName = abuseObj["contact"]["name"]

                # print(str(res))
                abuseEmail = getEmails(str(res))
                contacts[ip] = {"country": res["asn_country_code"],
                                "name": res["asn_description"],
                                "ip": ip, "email": abuseEmail}
            except HTTPLookupError as error:
                logging.error(str(error)+" : "+str(ip))

    # print(contacts)
    return ips, contacts
