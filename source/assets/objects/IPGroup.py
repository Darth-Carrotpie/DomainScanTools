class IPGroup():
    def __init__(self, ip):
        self.ips = []
        self.contacts = ""
        self.chunkName = ""
        self.chunkCountry = ""

    def addChunkLine(self, newLogLine):
        line = newLogLine
        if type(newLogLine) is list:
            line = ",".join(newLogLine)
        self.mylogs.append(line.rstrip())

    def setContacts(self, newContacts):
        self.contacts = newContacts
        if "name" in newContacts:
            self.chunkName = newContacts["name"]
        if "country" in newContacts:
            self.chunkCountry = newContacts["country"]

    def __str__(self):
        output = str(self.contacts) + "\n"
        for log in sorted(self.mylogs):
            output = output + log + "\n"
        return output
