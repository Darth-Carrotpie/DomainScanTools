class LogChunk():
    def __init__(self, ip):
        self.ip = ip
        self.logs = []
        self.contacts = ""
        self.chunkName = ""

    def addChunkLine(self, newLogLine):
        self.logs.append(newLogLine)

    def setContacts(self, newContacts):
        self.contacts = newContacts
        print("set new contact: "+newContacts["name"])
        self.chunkName = newContacts["name"]

    def __str__(self):
        output = self.contacts + "\n"
        for log in sorted(self.logs):
            output += log + "\n"
        return output
