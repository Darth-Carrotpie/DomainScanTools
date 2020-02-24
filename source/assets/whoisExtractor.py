from ipwhois import IPWhois


def getIpsAndContacts(urls):
    ips = {}

    for url in urls:
        try:
            ip = socket.gethostbyname(url.split("//", 1)[1].split("/", 1)[0])
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
        obj = IPWhois(ip)
        res = obj.lookup_rdap()
        # print(res)
        abuseEntity = res["entities"][len(res["entities"]) - 1]
        # print("abuse Entity: "+abuseEntity)
        abuseObj = res["objects"][abuseEntity]
        providerName = abuseObj["contact"]["name"]

        # print(str(res))
        abuseEmail = getEmails(str(res))
        contacts[ip] = {"country": res["asn_country_code"],
                        "name": providerName,
                        "description": res["asn_description"],
                        "ip": ip, "email": abuseEmail}
    # print(contacts)
    return ips, contacts
