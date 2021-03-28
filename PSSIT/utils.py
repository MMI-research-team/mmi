import sys
import os
import datetime as date
from argparse import ArgumentParser, ArgumentTypeError
from hashlib import sha3_224
import numpy as np

""" Check imports """


def checkImports(libraries):
    for libname in libraries:
        try:
            lib = __import__(libname)
        except:
            print(sys.exc_info())
            print("Nie można zaimportować biblioteki {}".format(libname))
            sys.exit()
        else:
            globals()[libname] = lib


"""  List files in specific directory """


def listFilesInPath(path):
    files = []
    try:
        for entry in os.listdir(path):
            if os.path.isfile(os.path.join(path, entry)):
                files.append(entry)
        return files
    except FileNotFoundError:
        raise FileNotFoundError("Nie można odnaleźć ścieżki")


""" Check if output directory exists """


def isOutputPathExists(outputPath):
    if (os.path.isdir(outputPath)):
        return True
    else:
        return False


""" Create output directory if that directory doesn't exists """


def createOutputPathDir(outputPath):
    absPath = os.path.abspath(outputPath)
    os.mkdir(absPath)


""" Check if output directory has a file inside """


def checkContentOfOutputPath(outputPath):
    filesList = os.listdir(os.path.abspath(outputPath))
    return len(filesList)


""" Remove all files in given directory """


def removeItemsFromDirectory(outputPath):
    for f in os.listdir(os.path.abspath(outputPath)):
        os.remove(os.path.join(outputPath, f))


""" Create log string """


def createLog(config, inputFile, outputFile, workTime):
    size1 = os.path.getsize(os.path.join(
        config['inputPath'], inputFile))
    size2 = os.path.getsize(os.path.join(
        config['outputPath'], "{}".format(outputFile)))
    log = "Input: {}, input size:{} bytes,action={},encoding={},time={},outputfile={},output size={} bytes,CR={}".format(
        inputFile, size1, config['action'], config['encoding'],
        round(workTime, 4), "{}".format(outputFile),
        size2, round((size2 / size1), 4)
    )
    return log


""" Save logs to file with current date as filename """


def saveLogsToFile(logs):
    if (os.path.isdir("logs") is False):
        os.mkdir("logs")
    actual_date = date.datetime.now()
    f = open("logs/{}.txt".format(actual_date.strftime("%Y-%m-%d-%H-%M-%S")),
             "w")
    for log in logs:
        f.write(log)
        f.write("\n")
    f.close()


def check_paramater_a_if_relative_first(a: int) -> int:
    temp_a = int(a)
    if np.gcd(temp_a, 256) == 1:
        return temp_a
    else:
        raise ArgumentTypeError(
            "Value of paramater a must be relative prime with 256")


def setup_cli():
    args_parser = ArgumentParser()
    args_parser.add_argument("--action", type=str, action="store",
                             help="Name for action", required=True,
                             choices=["encode", "decode"])
    args_parser.add_argument("-o", "--output", type=str,
                             action="store",
                             help="Path for output directory",
                             dest="outputPath",
                             required=True)
    args_parser.add_argument("-i", "--input", type=str, action="store",
                             dest="inputPath",
                             help="Path for input directory", required=True)
    args_parser.add_argument("-f", "--format", type=str, default="",
                             action="store",
                             choices=["png", "bmp", "sgi", "ppm", "tga", "ogg",
                                      "flac", "wma", "m4a", "wav"],
                             help="Extension for output file")
    args_parser.add_argument("-fT", "--fileType", type=str,
                             action="store", required=True,
                             help="File type of output file",
                             choices=["image", "sound"], dest="fileType")
    args_parser.add_argument("-e", "--encoding", type=str,
                             action="store", required=True,
                             help="Encoding of characters in input files",
                             choices=["utf8", "ascii"])
    args_parser.add_argument("--hash", action="store_true",
                             dest="isHash",
                             help="Information for script to use one-way hash "
                                  "function to convert output file name")
    args_parser.add_argument("-a", type=check_paramater_a_if_relative_first,
                             action="store",
                             help="Value of argument a", required=True)
    args_parser.add_argument("-b", type=int, action="store",
                             help="Value of argument b", required=True)
    return args_parser


def define_default_format_by_file_type(file_type: str) -> str:
    if file_type == "image":
        return "png"
    else:
        return "wav"


def get_arguments(args_parser):
    args = vars(args_parser.parse_args())
    args["inputPath"] = os.path.abspath(args["inputPath"])
    args["outputPath"] = os.path.abspath(args["outputPath"])

    if args["format"] == "":
        args["format"] = define_default_format_by_file_type(args["fileType"])
    return args


""" Read content from txt file"""


def readFileContent(inputPath, inputFile):
    with open(os.path.join(inputPath, inputFile), "r", encoding="utf8") as file:
        fileContent = file.readlines()
        textContent = ""
        for i in fileContent:
            textContent += i

        textContent += chr(3)
        textContent += inputFile
        textContent += chr(3)
    return textContent


""" Proces of cleaning DataOutputDirectory"""


def clearDirectory(outputPath):
    if isOutputPathExists(outputPath) == True:
        filesAmount = checkContentOfOutputPath(outputPath)
        if filesAmount > 0:
            print("Directory has files. Remove all files?[Y/N]")
            option = input()
            if option in ['Y', 'y']:
                removeItemsFromDirectory(outputPath)
                print("All files was removed")

    else:
        createOutputPathDir(outputPath)
        print("Created directory for output")


""" Hash filename with sha3_224"""


def hashFilename(filename):
    return str(sha3_224(filename.encode()).hexdigest())


def get_inverse_a(a):
    for i in range(256):
        if (a * i) % 256 == 1:
            return i


def get_inverse_a_sound(a):
    for i in range(256 ** 2):
        if (a * i) % (256 ** 2) == 1:
            return i
