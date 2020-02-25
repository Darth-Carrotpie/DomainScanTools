import re


def getEmails(s):
    # pylint: disable=no-member
    emailRegex = re.compile(
        (r"([a-z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`"
         r"{|}~-]+)*(@|\sat\s)(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?(\.|"
         r"\sdot\s))+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)"))
    return {email[0] for email in re.
            findall(emailRegex, s) if not email[0].startswith('//')}


def getFirstIP(s):
    return re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', s).group()
