# Project Title

TIFF to OCR PDF Application

## Description

* ocrmypdf, ghostscript, PyPDF2, glob library used
* OCR the TIFF Images
* Output format: Page wise PDF, Page wise PDF/A, Combined PDF, Combined PDF/A
* language will be defined in "lang.ini" file in the same path of input files.
* language code should be three digit iso code
* Multiple language should be add by separation of "+" symbol. e.g.: eng+dan

## Getting Started

### Dependencies

* Windows 7

### Installing

* pip install ocrmypdf
* pip install ghostscript
* pip install PyPDF2
* Tesseract version 5 should be installed in "C:\Program Files\Tesseract-OCR"

### Executing program

* "lang.ini" file should copied in the tool path
* Run the program
* Tool will ask to enter the path of the input TIF file
* Tool execute the TIFF file and create the output files
* PDF/A converted files will created in the "PDF-A" folder

### Help

* language will be defined in "lang.ini" file in the same path of input files.
* language code should be three digit iso code
* Multiple language should be add by separation of "+" symbol. e.g.: eng+dan



## Version History

* 0.1
    * Initial Release
