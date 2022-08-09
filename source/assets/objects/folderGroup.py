
def Intersection(lst1, lst2):
    return set(lst1).intersection(lst2)

def Intersections(listOfLists):
    return set.intersection(*map(set,listOfLists))

class FolderGroup():
    chunks = []
    ids = () #these are emails, but could be anything
    groupName = ""

    def __init__(self, chunks):
        self.chunks = chunks.copy()
        #print(type(chunks))
        #print(type(chunks[0]))
        emailList = [chunk.GetEmails() for chunk in self.chunks] 
        self.ids = set([x for l in emailList for x in l]) #combined emails
        #self.folderName = name

    def __str__(self):
        print("FolderGroup.name="+self.folderName)

    def AddChunk(self,newChunk):
        self.chunks.append(newChunk)
        self.ids.update(newChunk.GetEmails())
        self.ids = set(self.ids)


    def SimilarNotEqual(self, testChunk):
        if len(Intersection(testChunk.GetEmails(), self.ids)) > 0:
            return True
        return False

    def SetGroupName(self, setName = ""):
        if setName != "":
            self.groupName = setName
            return
        inters = Intersections([chunk.GetEmails() for chunk in self.chunks])
        if(len(inters) == 0):
            self.groupName = ""
        else:
            abuseM = [s for s in inters if "abuse" in s]
            newName = next(iter(abuseM)) if len(abuseM) > 0 else next(iter(inters))
            self.groupName = newName.replace("'", '').replace(" ", '')
    
    def IsSingle(self):
        if len(self.chunks) == 1:
            return True
        if len(set([chunk.chunkName for chunk in self.chunks])) == 1:
            return True
        return False

    def SaveGroup(self):
        fileNames = []
        if self.groupName == "":
            self.groupName = "EmptyName"
        for chunk in self.chunks:
            chunk.targetFolder = self.groupName
            filePathSaved = chunk.SaveChunkToFile()
            if filePathSaved != "":
                fileNames.append(filePathSaved)
        return fileNames
