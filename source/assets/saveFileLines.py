from os import path, makedirs
import __main__ as main


def saveLinesToOutput(lines, outputFileName, currentFolder):
    newFileName = "{}.txt".format(outputFileName).replace(
        " ", "_").replace("\\", "_").replace("-", "_").replace(",", "")

    curr_path = path.dirname(path.abspath(main.__file__))
    if currentFolder:
        abs_path = path.join(curr_path, "IO", currentFolder)
        if not path.exists(abs_path):
            makedirs(abs_path)
        abs_path = path.join(abs_path, newFileName)
    else:
        abs_path = path.join(curr_path, "IO", newFileName)
    # abs_path = path.join("IO", newFileName)
    # print("writing file to: "+abs_path)
    saveLines(abs_path, lines)
    return abs_path


def saveChunkToOutput(contacts, titlesLine, logs, fileNameToSave, targetFolder):
    newFileName = "{}.txt".format(fileNameToSave).replace(
        " ", "_").replace("\\", "_").replace("-", "_").replace(",", "")

    curr_path = path.dirname(path.abspath(main.__file__))
    if targetFolder:
        abs_path = path.join(curr_path, "IO", targetFolder)
        if not path.exists(abs_path):
            makedirs(abs_path)
        abs_path = path.join(abs_path, newFileName)
    else:
        abs_path = path.join(curr_path, "IO", newFileName)

    if not path.exists(abs_path):
        linesToSave = [str(contacts).replace("'", " ")]
        linesToSave.append(titlesLine)
        linesToSave.extend(logs)
        saveLines(abs_path, linesToSave)
        return abs_path
    else:
        addLines(abs_path, logs)
        return ""
    # print("writing file to: "+abs_path)

def saveLines(abs_path, lines):
    with open(abs_path, 'w') as output:
        for row in lines:
            output.write(str(row) + '\n')

def addLines(abs_path, lines):
    with open(abs_path, 'a') as output:
        for row in lines:
            output.write(str(row) + '\n')

def openOutput(outputFile):
    newFileName = "{}.txt".format(outputFile).replace(" ", "_")
    curr_path = path.dirname(path.abspath(main.__file__))
    abs_path = path.join(curr_path, "IO", newFileName)
    os.open(abs_path)
