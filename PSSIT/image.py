from PIL import Image
from hashlib import sha3_224
import numpy as np
import os
import random
import utils

"""Calculate image width and height based on text length"""


def calculateImageSize(textLength):
    length = int((textLength / 3) ** (0.5)) + 1

    imageWidth = random.randint(int(length * .75), int(length * 1.2))
    imageHeight = int(length ** 2 / imageWidth) + 1

    return imageWidth, imageHeight


""" Fill text for calculated size with random signs """


def fillTextWithRandomValues(textContent, imageWidth, imageHeight):
    while len(textContent) < imageWidth * imageHeight * 3:
        textContent.append(np.random.randint(32, 127))

    return textContent


"""Change letter to value needed for encoding data with utf8"""


def letterToNumbers(a, b, value):
    first = a * (value // 256) + b
    second = a * (value % 256) + b

    return first, second


def letterToNumber(a, b, value):
    return (a * value + b) % 256


"""Decode sign from given numbers for utf8 encoding"""


def numbersToLetter(inverse_a, b, sign1, sign2):
    sign1 = ((sign1 - b) * inverse_a) % 256
    sign2 = ((sign2 - b) * inverse_a) % 256
    return sign1 * 256 + sign2


def numberToLetter(inverse_a, b, sign):
    return ((sign - b) * inverse_a) % 256


"""Convert given text to array with pixels value"""


def convertTextToPNGFormat(textContent, imageWidth, imageHeight):
    pngPixels = np.asarray(textContent, dtype=np.uint8)

    pngPixels = pngPixels.reshape((imageHeight, imageWidth, 3))
    return pngPixels


"""Save pixels arr to image file"""


def saveAsPNG(filename, pixels, ):
    img = Image.fromarray(pixels)
    img.save(filename)


"""Convert pixels to text from image file for ascii encoding"""


def pngToASCIIText(inverse_a, b, filename, inputPath, outputPath):
    im = Image.open(os.path.join(inputPath, "{0}".format(filename)))

    data = np.asarray(im)

    pixels1d = data.flatten()
    decodedText = [chr(numberToLetter(inverse_a, b, i)) for i in pixels1d]
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


def pngToUTF8Text(params, filename, inputPath, outputPath):
    im = Image.open(os.path.join(inputPath, "{0}".format(filename)))
    data = np.asarray(im)

    pixels1d = data.flatten()

    firsts = pixels1d[::2]
    seconds = pixels1d[1::2]

    data_ = []

    for i, j in zip(firsts, seconds):
        data_.append(numbersToLetter(params[0], params[1], i, j))

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


def convertUtf8ToNumbers(a, b, text):
    numbers = []
    for i in text:
        numbers.extend(letterToNumbers(a, b, ord(i)))
    return numbers


def convertAsciiToNumbers(a, b, text):
    numbers = []
    for i in text:
        numbers.append(letterToNumber(a, b, ord(i)))
    return numbers

def saveTextFileAsImage(fileContent,outputFileNamePath):
    imageWidth, imageHeight = calculateImageSize(
        len(fileContent))
    pngFormat = fillTextWithRandomValues(
        fileContent, imageWidth, imageHeight)

    pngFormat = convertTextToPNGFormat(
        pngFormat, imageWidth, imageHeight)

    saveAsPNG(outputFileNamePath, pngFormat)