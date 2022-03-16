from assets.saveFileLines import saveChunkToOutput 

class LogChunk():
    def __init__(self, ip):
        self.ip = ip
        self.mylogs = []
        self.contacts = ""
        self.chunkName = ""
        self.chunkCountry = ""
        self.titlesLine = ""
        self.targetFolder = ""

    def setTitlesLine(self, newTitlesLine):
        self.titlesLine = newTitlesLine

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

    def GetEmails(self):
        return self.contacts["email"]

    def SaveChunkToFile(self):
        concacts = str(self.contacts).replace('"', "&%").replace("&%'", " ").replace("&%", " ")
        fileNameToSave = self.chunkCountry+"_"+self.chunkName[:15]

        #print("total logs to save: "+str(len(self.mylogs))+" in chunk file called:"+fileNameToSave)
        return saveChunkToOutput(concacts, self.titlesLine, self.mylogs, fileNameToSave, self.targetFolder)