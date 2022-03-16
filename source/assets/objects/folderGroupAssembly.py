from .folderGroup import FolderGroup


class FolderGroupAssembly():
    folderGroups = []
    chunks = []
    unfolderedChunks = []


    def __init__(self, ids, chunks):
        self.ids = set(ids)
        self.chunks = chunks

    def __str__(self):
        output = "ASN GroupAmount:"+str(len(self.folderGroups))+"\n"
        output += "IP ChunkAmount:"+str(len(self.chunks))+"\n"
        #output += "; ".join([str(gr) for gr in self.ids])
        return output

    def GroupNames(self):
        ouptut = "names:"
        ouptut+= "; ".join([str(gr.groupName) for gr in self.folderGroups])

    def Group(self):
        #print(next(iter(self.chunks)))
        for chunk in self.chunks:
            grouped = False
            for group in self.folderGroups:
                if group.SimilarNotEqual(chunk):
                    group.AddChunk(chunk)
                    grouped = True
            if not grouped:
                self.NewFolderGroup(list([chunk]))


    def NewFolderGroup(self, newChunks):
        self.folderGroups.append(FolderGroup(newChunks))

    def SaveGroupsToFile(self):
        fileNames = []
        for group in self.folderGroups:
            group.SetGroupName()

        self.SingleChunkGroups()

        for group in self.folderGroups:
            fileNames.extend(group.SaveGroup())
        return fileNames

    def SingleChunkGroups(self):
        singles = [gr for gr in self.folderGroups if len(gr.chunks) == 1]
        smallSingles, bigSingles = [], []
        for s in singles:
            (smallSingles if len(s.chunks[0].mylogs) <= 5 else bigSingles).append(s)
        for s in smallSingles:
            s.SetGroupName("_Small Singles")
        for s in bigSingles:
            s.SetGroupName("_Big Singles")