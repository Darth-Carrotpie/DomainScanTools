from ipwhois import IPWhois, HTTPLookupError
from assets.stringRegexHelper import getEmails
import socket
import logging


def getIpsAndContacts(urls, isIP):
    ips = {}

    for url in urls:
        try:
            if(isIP):
                ip = url
                # print("got ip: "+ip)
            else:
                ip = socket.gethostbyname(
                    url.split("//", 1)[1].split("/", 1)[0])
            if(ip not in ips):
                ips[ip] = [url]
            else:
                if(url not in ips[ip]):
                    ips[ip].append(url)
        except socket.gaierror as error:
            logging.error('could not get IP from socket of URL: ' +
                          url.split("//", 1)[1].split("/", 1)[0])
    contacts = {}
    for ip in ips:
        if(len(ip) > 7):
            # print("looking up: "+ip)
            try:
                obj = IPWhois(ip)
                res = obj.lookup_rdap(asn_methods=['dns', 'whois', 'http'])
                abuseEntity, abuseObj, providerName = ("",) * 3
                if(len(res["entities"]) > 0):
                    abuseEntity = res["entities"][len(res["entities"]) - 1]
                    abuseObj = res["objects"][abuseEntity]
                    if "contact" in abuseObj:
                        providerName = abuseObj["contact"]["name"]

                abuseEmail = getEmails(str(res))
                contacts[ip] = {"country": res["asn_country_code"],
                                "name": res["asn_description"],
                                "ip": ip, "email": abuseEmail}
            except Exception as e:
                logging.warning(str(e)+" : "+str(ip))
                # contacts[ip] = {}

    return ips, contacts
