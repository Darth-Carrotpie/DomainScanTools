from os import path, startfile
import __main__ as main


def saveLinesToOutput(lines, outputFileName):
    # print("trying to save...:")
    # print(urls)
    newFileName = "output {}.txt".format(outputFileName).replace(" ", "_")
    abs_path = path.join("IO", newFileName)
    with open(abs_path, 'w') as output:
        for row in lines:
            output.write(str(row) + '\n')
    return newFileName


def openOutput(outputFile):
    curr_path = path.dirname(path.abspath(main.__file__))
    abs_path = path.join(curr_path, "IO", outputFile)
    startfile(abs_path)
