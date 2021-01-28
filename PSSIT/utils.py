import sys
import os
import datetime as date
from hashlib import sha3_224

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
    f = open("logs/{}.txt".format(actual_date.strftime("%Y-%m-%d-%H-%M-%S")), "w")
    for log in logs:
        f.write(log)
        f.write("\n")
    f.close()


""" Check encoding from given value and return its value or default value
Values : utf8,ascii
Default value : utf8
 """


def checkEnconding(params, encoding):
    tempValue = ""
    if ("-encoding" in params.keys()):
        tempValue = params["-encoding"]

    if ("-e" in params.keys()):
        tempValue = params["-e"]
    if (tempValue in ['utf8', 'ascii']):
        return tempValue
    else:
        return encoding


""" Check input path from given value and return its value or default value of path """


def checkInputPath(params, inputPath):
    if ("-input" in params.keys()):
        inputPath = params["-input"]

    if ("-i" in params.keys()):
        inputPath = params["-i"]

    return os.path.abspath(inputPath)


""" Check output path from given value and return its value or default value of path """


def checkOutputPath(params, outputPath):
    if ("-output" in params.keys()):
        outputPath = params["-output"]

    if ("-o" in params.keys()):
        outputPath = params["-o"]

    return os.path.abspath(outputPath)


""" Check hash value from given value and return its value or default value of path
 Values : False,True
 Default Value : False
"""


def checkIsHash(params, isHash):
    tempValue = False
    if ("-hash" in params.keys()):
        tempValue = params["-hash"]

    if ("-h" in params.keys()):
        tempValue = params["-h"]
    if (tempValue in ["True", "False"]):
        return bool(tempValue)
    else:
        return isHash


""" Check action from given value and return that value or default value
Values : encode,decode
Default Value : encode """


def checkAction(params, action):
    tempAction = ""
    if ("-action" in params.keys()):
        tempAction = params["-action"]

    if ("-a" in params.keys()):
        tempAction = params["-a"]
    if (tempAction in ['encode', 'decode']):
        return tempAction
    else:
        return action


""" Get params dictionary  """


def getParams():
    tempParamsDict = {}
    params = sys.argv[1:]
    for i in params:
        param = i.split("=")
        tempParamsDict[param[0]] = param[1]
    return tempParamsDict


""" Init config with default values"""


def initConfig():
    config = {
        "encoding": "utf8",
        "inputPath": "DataInput",
        "outputPath": "DataOutput",
        "action": "encode",
        "isHash": False
    }
    return config


"""Create config with values from parameters """


def setup(params, config):
    config['inputPath'] = checkInputPath(params, config['inputPath'])
    config['outputPath'] = checkOutputPath(params, config['outputPath'])
    config['isHash'] = checkIsHash(params, config['isHash'])
    config['action'] = checkAction(params, config['action'])
    config['fileType'] = checkFileType(params)
    if (config['fileType'] == None):
        raise Exception("Unknown fileType",
                        "given fileType is different from permitted values")
    else:
        if (config['fileType'] == "sound"):
            config['format'] = "wav"
        else:
            config['format'] = "png"
            config['encoding'] = checkEnconding(params, config['encoding'])

    config['format'] = checkFormat(params, config['format'])
    return config


""" Check format from given value and return that value or default value from  """


def checkFormat(params, fileFormat):
    tempValue = fileFormat

    if ("-format" in params.keys()):
        tempValue = params["-format"]

    if ("-f" in params.keys()):
        tempValue = params["-f"]
    if (tempValue in ['ogg', 'wav', "flac", "wma", "m4a", "png", "bmp", 'sgi', 'ppm', 'tga']):
        return tempValue
    else:
        print("unknown format. Set default value")
        return fileFormat


""" Check outputType value and return value  """


def checkFileType(params):
    tempFileType = None

    if ("-fileType" in params.keys()):
        tempFileType = params['-fileType']
    if ("-fT" in params.keys()):
        tempFileType = params['-fT']
    if (tempFileType in ["sound", "image"]):
        return tempFileType
    else:
        return None


""" Recognise inputFormat by extension of file for decode"""


def recogniseFileType(file):
    extension = file.split(".")[1]
    if (extension in ['wav', 'ogg', 'm4a', 'wma']):
        return "sound"
    elif (extension in ['png', 'bmp', 'sgi', 'ppm', 'tga']):
        return "image"
    else:
        return None


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
    if (isOutputPathExists(outputPath) == True):
        filesAmount = checkContentOfOutputPath(outputPath)
        if (filesAmount > 0):
            print("Directory has files. Remove all files?[Y/N]")
            option = input()
            if (option in ['Y', 'y']):
                removeItemsFromDirectory(outputPath)
                print("All files was removed")

    else:
        createOutputPathDir(outputPath)
        print("Created directory for output")


""" Hash filename with sha3_224"""


def hashFilename(filename):
    return str(sha3_224(filename.encode()).hexdigest())
