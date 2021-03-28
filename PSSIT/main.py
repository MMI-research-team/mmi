import os

import utils
import sound
import image
import timeit

libraries = ['sys', 'os', 'time', 'numpy',
             'os', 'struct', 'PIL', 'hashlib', "pydub"]
utils.checkImports(libraries)
args_parser = utils.setup_cli()
config = utils.get_arguments(args_parser)
utils.clearDirectory(config['outputPath'])
inputFilesList = utils.listFilesInPath(config['inputPath'])
numberOfFiles = len(inputFilesList)
numberOfDoneFiles = 0
if config['action'] == "encode":

    if config['fileType'] == "image":

        for file in inputFilesList:

            filename = file.split(".")[0]

            
            fileContent = utils.readFileContent(config['inputPath'], file)

            if config['encoding'] == "ascii":
                preContent = image.convertAsciiToNumbers(config["a"],
                                                         config["b"],
                                                         fileContent)
            else:
                preContent = image.convertUtf8ToNumbers(config["a"],
                                                        config["b"],
                                                        fileContent)

            if config['isHash']:
                filename = utils.hashFilename(filename)
            outputFileName = "{}.{}".format(filename, config['format'])
            outputFileNamePath = os.path.join(config["outputPath"],
                                              "{}.{}".format(filename,
                                                             config["format"]))

            image.saveTextFileAsImage(preContent, outputFileNamePath)
            

            numberOfDoneFiles += 1
            print("{} of {} processed".format(
                numberOfDoneFiles, numberOfFiles))
            
    else:
        for file in inputFilesList:
            filename = file.split(".")[0]
            outputFileName = "{}.{}".format(filename, config['format'])
            
            fileContent = utils.readFileContent(config['inputPath'], file)

            fileContent = sound.fillFileContent(fileContent)

            transformedFileContent = sound.transformFileContentToBytes(
                fileContent, config["a"], config["b"])

            sound.saveBytestoSoundFile(transformedFileContent, filename,
                                       config['outputPath'], config['format'])

            

            numberOfDoneFiles += 1
            print("{} of {} processed".format(
                numberOfDoneFiles, numberOfFiles))
            
if config['action'] == "decode":

    if config['fileType'] == "image":
        outputFileName = ""
        inverse_a = utils.get_inverse_a(config["a"])
        for file in inputFilesList:
            
            if config['encoding'] == "ascii":
                outputFileName = image.pngToASCIIText(
                    inverse_a, config["b"], file, config['inputPath'],
                    config['outputPath'])

            else:

                outputFileName = image.pngToUTF8Text([inverse_a, config["b"]],
                                                     file, config['inputPath'],
                                                     config['outputPath'])
            

            numberOfDoneFiles += 1
            print("{} of {} processed".format(
                numberOfDoneFiles, numberOfFiles))
            
    else:
        inverse_a = utils.get_inverse_a_sound(config["a"])
        for file in inputFilesList:
            
            soundContent = sound.readBytesFromSoundFile(
                file, config['inputPath'])
            transformedSoundFileContent = sound.transformBytesToText(
                soundContent, inverse_a, config["b"])
            outputFileName = sound.saveTextToFile(
                transformedSoundFileContent, config['outputPath'])
           

            numberOfDoneFiles += 1
            print("{} of {} processed".format(
                numberOfDoneFiles, numberOfFiles))
            
        
