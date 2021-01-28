import utils
import sound
import image

libraries = ['sys', 'os', 'time', 'numpy',
             'os', 'struct', 'PIL', 'hashlib', "pydub"]
utils.checkImports(libraries)
params = utils.getParams()
config = utils.initConfig()
utils.setup(params, config)
utils.clearDirectory(config['outputPath'])

inputFilesList = utils.listFilesInPath(config['inputPath'])
numberOfFiles = len(inputFilesList)
numberOfDoneFiles = 0
if (config['action'] == "encode"):

    if (config['fileType'] == "image"):

        for file in inputFilesList:

            filename = file.split(".")[0]

            fileContent = utils.readFileContent(config['inputPath'], file)

            if (config['encoding'] == "ascii"):
                preContent = image.convertAsciiToNumbers(fileContent)
            else:
                preContent = image.convertUtf8ToNumbers(fileContent)
            imageWidth, imageHeight = image.calculateImageSize(
                len(preContent))
            pngFormat = image.fillTextWithRandomValues(
                preContent, imageWidth, imageHeight)

            pngFormat = image.convertTextToPNGFormat(
                pngFormat, imageWidth, imageHeight)

            if (config['isHash']):
                filename = utils.hashFilename(filename)

            image.saveAsPNG(filename, config['outputPath'], pngFormat,
                            imageWidth, config['format'])

            outputFileName = "{}.{}".format(filename, config['format'])

            numberOfDoneFiles += 1
            print("{} of {} processed".format(
                numberOfDoneFiles, numberOfFiles))
    else:
        for file in inputFilesList:

            filename = file.split(".")[0]

            fileContent = utils.readFileContent(config['inputPath'], file)

            fileContent = sound.fillFileContent(fileContent)

            transformedFileContent = sound.transformFileContentToBytes(
                fileContent)

            sound.saveBytestoSoundFile(transformedFileContent, filename,
                                       config['outputPath'], config['format'])

            outputFileName = "{}.{}".format(filename, config['format'])

            numberOfDoneFiles += 1
            print("{} of {} processed".format(
                numberOfDoneFiles, numberOfFiles))


if (config['action'] == "decode"):

    if (config['fileType'] == "image"):
        for file in inputFilesList:

            if (config['encoding'] == "ascii"):
                outputFilename = image.pngToASCIIText(
                    file, config['inputPath'], config['outputPath'])

            else:

                outputFilename = image.pngToUTF8Text(
                    file, config['inputPath'], config['outputPath'])

            numberOfDoneFiles += 1
            print("{} of {} processed".format(
                numberOfDoneFiles, numberOfFiles))
    else:
        for file in inputFilesList:

            soundContent = sound.readBytesFromSoundFile(
                file, config['inputPath'])
            transformedSoundFileContent = sound.transformBytesToText(
                soundContent)
            outputFilename = sound.saveTextToFile(
                transformedSoundFileContent, config['outputPath'])

            numberOfDoneFiles += 1
            print("{} of {} processed".format(
                numberOfDoneFiles, numberOfFiles))
