from os import path, startfile
import __main__ as main


def saveLinesToOutput(lines, outputFile):
    # print("trying to save...:")
    # print(urls)
    with open(outputFile, 'w') as output:
        for row in lines:
            output.write(str(row) + '\n')


def openOutput(outputFile):
    curr_path = path.dirname(path.abspath(main.__file__))
    abs_path = path.join(curr_path, "IO/output.txt")
    startfile(abs_path)
