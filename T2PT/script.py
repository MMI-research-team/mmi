import sys
import os
import numpy as np
from PIL import Image
from hashlib import sha3_224

# Starting setup
# Variables
config = {}
config['inputPath'] = "DataInput"
config['outputPath'] = "DataOutput"
config['isHash'] = False
config['encoding'] = "utf8"
config['action'] = "encode"
params = sys.argv[1:]
params_dict = {}
# Functions


def checkEnconding(params, encoding):
    tempValue = ""
    if("-encoding" in params.keys()):

        tempValue = params["-encoding"]

    if("-e" in params.keys()):

        tempValue = params["-e"]
    if(tempValue in ['utf8', 'ascii']):
        return tempValue
    else:
        return encoding


def checkInputPath(params, inputPath):
    if("-input" in params.keys()):

        inputPath = params["-input"]

    if("-i" in params.keys()):

        inputPath = params["-i"]

    return os.path.abspath(inputPath)


def checkOutputPath(params, outputPath):
    if("-output" in params.keys()):

        outputPath = params["-output"]

    if("-o" in params.keys()):

        outputPath = params["-o"]

    return os.path.abspath(outputPath)


def checkIsHash(params, isHash):
    tempValue = False
    if("-hash" in params.keys()):

        tempValue = params["-hash"]

    if("-h" in params.keys()):

        tempValue = params["-h"]
    if(tempValue in ["True", "False"]):
        return bool(tempValue)
    return isHash


def checkAction(params, action):
    tempValue = ""
    if("-action" in params.keys()):

        tempValue = params["-action"]

    if("-a" in params.keys()):

        tempValue = params["-a"]
    if(tempValue in ['encode', 'decode']):
        return tempValue
    return action

# Read files from given path


def listFilesInPath(path):
    files = []
    for entry in os.listdir(path):
        if os.path.isfile(os.path.join(path, entry)):
            files.append(entry)
    return files


def setup(params, config):
    config['encoding'] = checkEnconding(params, config['encoding'])
    config['inputPath'] = checkInputPath(params, config['inputPath'])
    config['outputPath'] = checkOutputPath(params, config['outputPath'])
    config['isHash'] = checkIsHash(params, config['isHash'])
    config['action'] = checkAction(params, config['action'])
    return config


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


def calculateImageSizeForASCII(textLength):
    imageSize = int(np.ceil((textLength/3) ** (0.5)))
    return imageSize


def calculateImageSizeForUTF8(textLength):
    imageSize = int(np.ceil((textLength*2/3) ** (0.5)))
    return imageSize


def fillTextContentASCII(textContent, imageSize):

    while len(textContent) < (imageSize**2)*3:
        textContent += chr(np.random.randint(32, 127))

    return textContent


def fillTextContentUTF8(textContent, imageSize):

    while len(textContent) < (imageSize**2)/2*3:
        textContent += chr(np.random.randint(32, 127))

    return textContent


def letterToHex(value):
    return value // 256, value % 256


def signsToHex(sign1, sign2):
    return sign1*256+sign2


def convertAsciiToPNGFormat(textContent):
    firsts = textContent[::3]
    seconds = textContent[1::3]
    thirds = textContent[2::3]
    pngPixels = []
    for i, j, k in zip(firsts, seconds, thirds):
        pngPixels.append([ord(i), ord(j), ord(k)])
    return pngPixels


def convertUTF8ToPNGFormat(textContent):
    tempTextContent = []

    for i in textContent:
        tempTextContent.extend(letterToHex(ord(i)))
    textContent = tempTextContent

    firsts = textContent[::3]
    seconds = textContent[1::3]
    thirds = textContent[2::3]
    pngPixels = []
    for i, j, k in zip(firsts, seconds, thirds):
        pngPixels.append([i, j, k])
    return pngPixels


def saveAsPNG(filename, outputPath, pixels, textLength, isHash):
    im = np.zeros((textLength, textLength, 3), dtype=np.uint8)
    img = Image.fromarray(im)

    row = 0
    column = 0
    element = 0

    while element < len(pixels):
        row = element // textLength
        column = element % textLength
        img.putpixel((row, column), tuple(pixels[element]))
        element += 1

    if(isHash):
        filename = str(sha3_224(filename.encode()).hexdigest())
    img.save(os.path.join(outputPath, "{0}.png".format(filename)))


def isOutputPathExists(outputPath):
    if(os.path.isdir(outputPath)):
        return True
    else:
        return False


def createOutputPathDir(outputPath):
    absPath = os.path.abspath(outputPath)
    os.mkdir(absPath)


def checkContentOfOutputPath(outputPath):
    filesList = os.listdir(os.path.abspath(outputPath))
    return len(filesList)


def clearDirectory(outputPath):
    for f in os.listdir(os.path.abspath(outputPath)):

        os.remove(os.path.join(outputPath, f))

# Convert png to txt file


def pngToASCIIText(filename, inputPath, outputPath):
    im = Image.open(os.path.join(inputPath, "{0}".format(filename)))
    px = im.load()
    text = ""
    pixels_ = []
    width, heigth = im.size
    for x in range(width):
        for y in range(heigth):
            pixels_.append(chr(px[x, y][0]))
            pixels_.append(chr(px[x, y][1]))
            pixels_.append(chr(px[x, y][2]))

        text = "".join(pixels_)
    contents = text.split(chr(3))
    outputFileName = contents[1]
    textContent = contents[0]

    f = open("{0}/{1}".format(outputPath, outputFileName),
             "w", encoding='utf8')
    f.write(textContent)
    f.close()


def pngToUTF8Text(filename, inputPath, outputPath):

    im = Image.open(os.path.join(inputPath, "{0}".format(filename)))
    px = im.load()

    width, heigth = im.size

    text = ""
    pixels_ = []
    for x in range(width):
        for y in range(heigth):
            pixels_.extend(px[x, y])

    a = pixels_[::2]
    b = pixels_[1::2]

    for i, j in zip(a, b):
        text += chr(signsToHex(i, j))

    contents = text.split(chr(3))
    outputFileName = contents[1]
    textContent = contents[0]

    f = open("{0}/{1}".format(outputPath, outputFileName),
             "w", encoding='utf8')
    f.write(textContent)
    f.close()


def convertASCIIToPNG(file, config):
    fileContent = readFileContent(config['inputPath'], file)
    imageSize = calculateImageSizeForASCII(len(fileContent))

    fileContent = fillTextContentASCII(fileContent, imageSize)
    pngFormat = convertAsciiToPNGFormat(fileContent)
    saveAsPNG(file, config['outputPath'], pngFormat,
              imageSize, config['isHash'])


def convertUTF8ToPNG(file, config):
    fileContent = readFileContent(config['inputPath'], file)

    imageSize = calculateImageSizeForUTF8(len(fileContent))

    fileContent = fillTextContentUTF8(fileContent, imageSize)

    pngFormat = convertUTF8ToPNGFormat(fileContent)
    saveAsPNG(file, config['outputPath'], pngFormat,
              imageSize, config['isHash'])


def decodePNGToAscii(file, config):

    pngToASCIIText(file, config['inputPath'], config['outputPath'])


def decodePNGToUTF8(file, config):

    pngToUTF8Text(file, config['inputPath'], config['outputPath'])


# Main program
# Get arguments from command line
for i in params:
    param = i.split("=")
    params_dict[param[0]] = param[1]

config = setup(params_dict, config)
inputFilesList = listFilesInPath(config['inputPath'])
if(isOutputPathExists(config['outputPath']) == True):
    filesAmount = checkContentOfOutputPath(config['outputPath'])
    if(filesAmount > 0):
        print("Directory has files. Remove all files?[Y/N]")
        option = input()
        if(option is "Y"):
            clearDirectory(config['outputPath'])

else:
    createOutputPathDir(config['outputPath'])

if(config['action'] == "encode"):
    if(config['encoding'].lower() == "utf8"):
        for file in inputFilesList:

            convertUTF8ToPNG(file, config)

    else:
        for file in inputFilesList:

            convertASCIIToPNG(file, config)

else:
    if(config['encoding'].lower() == "utf8"):
        for file in inputFilesList:

            decodePNGToUTF8(file, config)

    else:
        for file in inputFilesList:

            decodePNGToAscii(file, config)
print("Done")
