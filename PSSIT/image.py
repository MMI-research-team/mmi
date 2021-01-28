from PIL import Image
from hashlib import sha3_224
import numpy as np
import os
import random

"""Calculate image width and height based on text length"""

def calculateImageSize(textLength):
    length = int((textLength / 3) ** (0.5)) + 1

    imageWidth = random.randint(int(length*.75), int(length*1.2))
    imageHeight = int(length**2 / imageWidth) + 1

    return imageWidth, imageHeight


""" Fill text for calculated size with random signs """

def fillTextWithRandomValues(textContent, imageWidth, imageHeight):

    while len(textContent) < imageWidth*imageHeight*3:
        textContent.append(np.random.randint(32, 127))

    return textContent


"""Change letter to value needed for encoding data with utf8"""


def letterToNumbers(value):
    return value // 256, value % 256


"""Decode sign from given numbers for utf8 encoding"""


def numbersToLetter(sign1, sign2):
    return sign1*256+sign2


"""Convert given text to array with pixels value"""


def convertTextToPNGFormat(textContent, imageWidth, imageHeight):
   

    pngPixels = np.asarray(textContent, dtype=np.uint8)

    pngPixels = pngPixels.reshape((imageHeight, imageWidth, 3))
    return pngPixels


"""Save pixels arr to image file"""


def saveAsPNG(filename, outputPath, pixels, textLength, fileFormat):

    img = Image.fromarray(pixels)
    img.save(os.path.join(outputPath, "{}.{}".format(filename, fileFormat)))


"""Convert pixels to text from image file for ascii encoding"""


def pngToASCIIText(filename, inputPath, outputPath):
    im = Image.open(os.path.join(inputPath, "{0}".format(filename)))

    data = np.asarray(im)

    pixels1d = data.flatten()
    decodedText = [chr(i) for i in pixels1d]
    text = ''.join(decodedText)
    contents = text.split(chr(3))
    outputFileName = contents[1]
    textContent = contents[0]

    f = open("{0}/{1}".format(outputPath, outputFileName),
             "w", encoding='utf8')
    f.write(textContent)
    f.close()

    return outputFileName


"""Convert pixels to text from image file for utf8 encoding"""


def pngToUTF8Text(filename, inputPath, outputPath):

    im = Image.open(os.path.join(inputPath, "{0}".format(filename)))
    data = np.asarray(im)

    pixels1d = data.flatten()

    firsts = pixels1d[::2]
    seconds = pixels1d[1::2]

    data_ = []

    for i, j in zip(firsts, seconds):
        data_.append(numbersToLetter(i, j))

    decodedText = [chr(i) for i in data_]
    text = ''.join(decodedText)
    contents = text.split(chr(3))
    outputFileName = contents[1]
    textContent = contents[0]
   
    f = open("{0}/{1}".format(outputPath, outputFileName),
             "w", encoding='utf8')
    f.write(textContent)
    f.close()

    return outputFileName

def convertUtf8ToNumbers(text):
    numbers = []
    for i in text:
        numbers.extend(letterToNumbers(ord(i)))
    return numbers


def convertAsciiToNumbers(text):
    numbers = []
    for i in text:
        numbers.append(ord(i))
    return numbers