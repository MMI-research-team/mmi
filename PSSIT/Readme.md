## Steganography: Hiding Text in Image and Sound

#### Authors

- Marcin Lawnik
- Artur Pełka
- Adrian Kapczyński

#### Description

This script is a tool that allows you to encode text from a text file in a new
medium, which can be a graphic file or a sound file. The output file is created
based on the input file that provides the content for the media. The program
supports text files in **extended Ascii** and **UTF8** encoding. The second
function of the program is to recover the contents of a text file from image and
sound files.

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

| Name            | Default value | Call options    | Allowed values                                                               | Description                                                                                                                                      | Required |
| --------------- | ------------- | --------------- | ---------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ | -------- |
| Action          | -             | --action        | encode, decode                                                               | Defines the operations to be performed.                                                                                                          | Yes      |
| Input           | -             | --input, -i     | -                                                                            | Path to the directory with input files. If the path has spaces in it, the path shall be put in quotation marks                                   | Yes      |
| Output          | -             | --output, -o    | -                                                                            | Directory path for output files. If the path has spaces in it, the path shall be put in quotation marks.                                         | Yes      |
| Hash            | False         | --hash          | True, False                                                                  | Information for the script whether the output file name is to be converted using a one-way hash function.                                        | No       |
| Encoding        | -             | --encoding,-e   | utf8, ascii                                                                  | Defines the encoding of input files.                                                                                                             | Yes      |
| Format          | wav,png       | --format, -f    | png, bmp, sgi, ppm, tga,ogg, wav, flac, wma, m4a                             | Defines the output file format. The format depends on the type of output file.                                                                   | No       |
| Output filetype | -             | --fileType, -fT | image, sound                                                                 | Defines the output file type for the encode operation and the input file for the decode operation. It is used to select file processing methods. | Yes      |
| A               | -             | -a              | a must meet the condition for image gcd(a,256) = 1, for sound gcd(a,256^2)=1 |                                                                                                                                                  | Yes      |
| B               | -             | -b              | Every natural number                                                         |                                                                                                                                                  | Yes      |

#### Script execution

**Before running the script**

Make sure that Python version 3.x is installed as well as all libraries that are
needed.

To run the script, execute the command

```bash
python main.py -i=DataInput -o=DataOutput --action=encode --fileType=image -a=7 -b=3 -e=utf8
```

Sample commands with parameters

```bash
python main.py --fileType=sound --action=decode -i=DataOutput -o=DataReverse -e=utf8 -a=7 -b=3 -e=utf8

```

#### License

Shield: [![CC BY 4.0][cc-by-shield]][cc-by]

This work is licensed under
a [Creative Commons Attribution 4.0 International License][cc-by].

[![CC BY 4.0][cc-by-image]][cc-by]

[cc-by]: http://creativecommons.org/licenses/by/4.0/
[cc-by-image]: https://i.creativecommons.org/l/by/4.0/88x31.png
[cc-by-shield]: https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg
