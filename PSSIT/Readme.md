## Steganography: Hiding Text in Image and Sound

#### Authors

- Marcin Lawnik
- Artur Pełka
- Adrian Kapczyński

#### Description

This script is a tool that allows you to encode text from a text file in a new medium, which can be a graphic file or a sound file. 
The output file is created based on the input file that provides the content for the media. The program supports text files in **extended Ascii** and ** UTF8 ** encoding. The second function of the program is to recover the contents of a text file from image and sound files.

#### Technologies/Libraries

- Python
- numpy
- hashlib
- PIL(Python Imaging Library)
- pydub(MIT License)

#### Supported file formats

Graphic files:

- PNG
- BMP
- SGI
- PPM
- TGA

Sound files:

- OGG
- WAV
- FLAC
- WMA
- M4A

#### Parameters

| Name            | Default value | Call options   | Allowed values                                   | Description                                                                                                                                      | Is required? |
| --------------- | ------------- | -------------- | ------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------ | ------------ |
| Action          | encode        | -action, -a    | encode, decode                                   | Defines the operations to be performed.                                                                                                          | No           |
| Input           | DataInput     | -input, -i     | -                                                | Path to the directory with input files. If the path has spaces in it, the path shall be put in quotation marks                                   | No           |
| Output          | DataOutput    | -output, -o    | -                                                | Directory path for output files. If the path has spaces in it, the path shall be put in quotation marks.                                         | No           |
| Hash            | False         | -hash, -h      | True, False                                      | Information for the script whether the output file name is to be converted using a one-way hash function.                                        | No           |
| Encoding        | utf8          | -encoding,-e   | utf8, ascii                                      | Defines the encoding of input files.                                                                                                             | No           |
| Format          | wav,png       | -format, -f    | png, bmp, sgi, ppm, tga,ogg, wav, flac, wma, m4a | Defines the output file format. The format depends on the type of output file.                                                                   | No           |
| Output filetype | -             | -fileType, -fT | image, sound                                     | Defines the output file type for the encode operation and the input file for the decode operation. It is used to select file processing methods. | Yes          |

#### Script execution

**Before running the script**

Make sure that Python version 3.x is installed as well as all  libraries that are needed.

To run the script, execute the command

```bash
python main.py -fileType=image
```

After the file name, fileType along with the valueone must defined. Further parameters are optional and have a default value.

Sample commands with parameters

```bash
python main.py -fileType=sound -format=m4a
```

```bash
python main.py -fileType=sound -a=decode -i=DataOutput -o=DataReverse

```

#### License

Shield: [![CC BY 4.0][cc-by-shield]][cc-by]

This work is licensed under a [Creative Commons Attribution 4.0 International
License][cc-by].

[![CC BY 4.0][cc-by-image]][cc-by]

[cc-by]: http://creativecommons.org/licenses/by/4.0/
[cc-by-image]: https://i.creativecommons.org/l/by/4.0/88x31.png
[cc-by-shield]: https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg
