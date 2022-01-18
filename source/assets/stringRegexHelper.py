import re
import logging


def getEmails(s):
    # pylint: disable=no-member
    emailRegex = re.compile(
        (r"([a-z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`"
         r"{|}~-]+)*(@|\sat\s)(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?(\.|"
         r"\sdot\s))+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)"))
    return {email[0].replace("'", "") for email in re.
            findall(emailRegex, s) if not email[0].startswith('//')}


def getFirstIP(s):
    try:
        return re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', ''.join(s)).group()
    except:
        None


def getIPFromLine(s, ipNo):
    ipRegex = re.compile(
        r"\b(?:(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}"
        r"(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\b"
    )
    try:
        #print("regex in ", ''.join(s))
        m = re.findall(ipRegex, ''.join(s))
        # print(m)
        return m[ipNo-1]
    except:
        logging.warning(
            'Could not get [{}] IP log line, must be title line!'.format(ipNo))
        return None
