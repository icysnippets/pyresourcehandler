# pyResourceHandler: Small package to help with resource handling 

pyResourceHandler provides a few functions to easily handle resources.

It requires Python 3.9+ to run.

## Key Features
* Small package
* 100% coverage
* Easy to use 
* Functions are type-hinted.
* Handles regular files, directories and even malformed python files as resources/assets.

## How to Install
Install from PyPi 
> pip install pyResourceHandler
   
Import 'extractFile' and/or 'extractDir' 
> from pyResourceHandler import extractFile
> 
## How to Use

1.The module should have a root directory with one of the following names:

* data
* resources
* assets

2.Place files and/or directories within your resource directory.

3.Done!

* To extract a file

> extractFile(
    "Example_Module",
    "file_example.txt",
    r"C:\Users\user\Desktop\your_file.txt"
)

* To extract a directory

> extractDirectory(
    "Example_Module",
    "directory_example",
    r"C:\Users\user\Desktop\your_directory"
)

1st Argument - Module import as a string.\
2nd Argument - Path to file/directory\
3rd Argument - Output path for file/directory

Do note, the above functions will not overwrite an existing file by default.\
To enable overwriting, set the argument named **overwrite** argument to True when invoking the functions.

## Why?

Writing similar pieces of code to access non-Python files across projects can be tedious.

This reduces boilerplate code for repetitive operations down to a single function call.

