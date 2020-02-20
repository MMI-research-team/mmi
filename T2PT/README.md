## T2PT
#### Authors
- Marcin Lawnik
- Artur Pełka
- Adrian Kapczyński
#### Description
The script is an implementation of a new method for storing text using images. The user converts the content of the text file into graphic format (RGB) and from the received values an image is generated. It is possible to reverse the operation to get a text file with the content from the image. The method supports encoding such as: **extended ASCII** and **UTF8**. Using this method allows you to hide the contents of the file and reduce the amount of file size that stores information.

#### Technologies
- Python
- numpy
- hashlib
- PIL(Python Imaging Library)
#### Parameters
| Name     | Default value | Call options | Allowed values | Description                                                                                                                 |
| -------- | ------------- | ------------ | -------------- | --------------------------------------------------------------------------------------------------------------------------- |
| Action   | encode        | -action, -a  | encode, decode | The task that the script will perform    .                                                                                  |
| Input    | DataInput     | -input, -i   | -              | Path to the folder with input files. The path should be between the "" characters. By default this is the DataInput folder. |
| Output   | DataOutput    | -output, -o  | -              | Path to the folder for input files. The path should be between the characters "". The default is the DataOutput folder.     |
| Hash     | False         | -hash, -h    | True, False    | Information for the script if the PNG file name is to be a hash or the same as for the input file .                         |
| Encoding | utf8          | -encoding,-e | utf8, ascii    | Parameter indicating the encoding of input files.                                                                           |

#### Launch
**Before launch** 

Make sure you have the necessary dependencies and the Python interpreter installed.
To run the script, execute the command
```bash
python script.py
```
After the file name, you can specify parameters with values. If you don't specify any of the parameters, the default value will be assigned to it.

Example of launch with parameters
```bash
python script.py -a=encode -h=True -input="Data/ImageSource"
```
#### License
Shield: [![CC BY 4.0][cc-by-shield]][cc-by]

This work is licensed under a [Creative Commons Attribution 4.0 International
License][cc-by].

[![CC BY 4.0][cc-by-image]][cc-by]

[cc-by]: http://creativecommons.org/licenses/by/4.0/
[cc-by-image]: https://i.creativecommons.org/l/by/4.0/88x31.png
[cc-by-shield]: https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg

