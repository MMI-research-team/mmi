import os
from pydub import AudioSegment
import struct
import numpy as np
import utils

"""Fill content from text file with 'a' letter to required size"""


def fillFileContent(fileContent):
    textLength = len(fileContent)
    rest = textLength % 4
    if (rest != 0):
        fileContent += chr(3)
        for i in range(rest - 1):
            fileContent += chr(97)
    return fileContent


""" Read bytes from sound file """


def readBytesFromSoundFile(filename, inputPath):
    soundFile = AudioSegment.from_file(os.path.join(
        inputPath, filename))
    fileContent = soundFile.raw_data
    return fileContent


""" Transform sign to number representation """


def transformSignToNumber(letter, a, b):
    num_letter = ord(letter)

    new_number = ((a * num_letter) + b) % 256 ** 2
    return new_number


""" Transform number representation to sign"""


def transformNumberToSign(number, inverse_a, b):
    new_number = ((number - b) * inverse_a) % 256 ** 2

    return chr(new_number)


""" Transform file content to bytes arr"""


def transformFileContentToBytes(fileContent, a, b):
    tempArr = []
    for i in range(len(fileContent)):
        packedValue = struct.pack('H',
                                  transformSignToNumber(fileContent[i], a, b))
        tempArr.append(packedValue)
    return np.array(tempArr).tobytes()


""" Transform bytes arr to text"""


def transformBytesToText(bytes_arr, inverse_a, b):
    content = ""
    dane_i = [int.from_bytes(bytes_arr[2 * i:2 * i + 2], "little")
              for i in range(int(len(bytes_arr) / 2))]

    for i in dane_i:
        content += transformNumberToSign(i, inverse_a, b)
    return content


""" Save bytes arr to sound file"""


def saveBytestoSoundFile(bytes_arr, file, outputPath, fileFormat):
    soundFile = AudioSegment(bytes_arr, sample_width=2,
                             channels=2, frame_rate=44100)
    fileStr = os.path.join(outputPath, "{}.{}".format(file, fileFormat))
    soundFile.export(fileStr, format="wav")


""" Save text to output file"""


def saveTextToFile(textContent, outputPath):
    contents = textContent.split(chr(3))
    file = "{}".format(contents[1])

    with open(os.path.join(outputPath, file), "w", encoding="utf8") as f:
        f.write(contents[0])

    return file
