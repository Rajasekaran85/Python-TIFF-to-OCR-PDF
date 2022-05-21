import sys
import os
import shutil
from PIL import Image
import ocrmypdf
import ghostscript
from PyPDF2 import PdfFileMerger
import glob

print("\n TIFF to OCR PDF & PDF/A Conversion \n")
print("\n Developed by A Rajasekaran\n")
print("\n Date: 20 May 2022 \n\n")


'''
- Getting the Input file path from user
- creating the "PDF-A" directory for store the PDF/A output files
- language will be defined in "lang.ini" file in the same path of input files.
- language code should be three digit iso code, multiple language should be add by separation	of "+" symbol. e.g.: eng+hin
- Tesseract version 5 should be installed in "C:\Program Files"
'''

filepath1 = input(" Enter the File path: ")

filepath = filepath1 + "\\"

filelist = os.path.isdir(filepath) # specified path is an existing directory or not

directory = "PDF-A"

PDF_A = filepath + directory

if os.path.exists(PDF_A):
    pass
else:
    os.mkdir(PDF_A)

langu = filepath + "lang.ini"



'''
- OCR the TIFF images
- Saved as page level PDF
- PDF file will be in png format, so the file size will be large
'''
for fname in os.listdir(filepath):
    print(fname)
    if not fname.endswith(".tif"):
        continue
    input_file = os.path.join(filepath, fname) 
    im1 = Image.open(input_file).convert("RGB")
    pname = os.path.splitext(fname)[0]
    output_file = filepath + pname + ".pdf"
    f1 = open(output_file, "w+b")
    with open(langu) as f:   # open the ini file
        ini = f.read()       # read the ini file
    ocrmypdf.ocr(input_file, output_file, language=ini, force_ocr=True, output="pdf", jpeg_quality="100")
    f1.close()




'''
- PDF files will changed to optimized format (JPEG compression) and fastweb view
'''
for fname in os.listdir(filepath):
    print(fname)
    if not fname.endswith(".pdf"):
        continue
    path = os.path.join(filepath, fname) 
    #print(fname)
    ghostScriptExec = ['gs', '-dBATCH', '-dNOPAUSE', '-dUseCIEColor', '-sProcessColorModel=DeviceRGB', '-dCompatibilityLevel=1.5', '-dJPEGQ=100', 
                   '-sDEVICE=pdfwrite', '-dFastWebView', '-sOutputFile='+ filepath + 'Page-' + fname, path]
    ghostscript.Ghostscript(*ghostScriptExec)
    print("\n Conversion Completed\n")



'''
- remove the png compression type pdf files
'''
for fname in os.listdir(filepath):
    if not fname.endswith(".tif"):
        continue
    pname1 = os.path.splitext(fname)[0]
    #print(pname1)
    delete = filepath + pname1 + ".pdf"
    os.remove(delete)



'''
- PDF/A output generation - PDF/A format "1b"
'''
for fname in os.listdir(filepath):
    print(fname)
    if not fname.endswith(".pdf"):
        continue
    path = os.path.join(filepath, fname) 
    print(path)
    
    #print(fname)
    #print(path)
    output_files = filepath + directory
    ghostScriptExec = ['gs', '-dPDFA', '-dBATCH', '-dNOPAUSE', '-dUseCIEColor', '-sProcessColorModel=DeviceRGB',
                   '-sDEVICE=pdfwrite', '-dFastWebView', '-sPDFACompatibilityPolicy=1',
                   '-sOutputFile='+ output_files + "/" + 'PDFA-' + fname, path]
    ghostscript.Ghostscript(*ghostScriptExec)
    #print(filepath)
    print("\n Conversion Completed\n")




'''
- Book level generation
- same PDF/A format
'''
collate_pdf = filepath + "/" + "collate.pdf"
bookpdfpath = filepath + "/" + "combined_pdf.pdf"
merger = PdfFileMerger()
for file in glob.glob(filepath + "*.pdf"): # glob module is used to match the files type
    #print(file)
    merger.append(file)
merger.write(collate_pdf)
merger.close()
ghostScriptExec = ['gs', '-dBATCH', '-dNOPAUSE', '-dUseCIEColor', '-sProcessColorModel=DeviceRGB', '-dCompatibilityLevel=1.5', '-dJPEGQ=100', 
                   '-sDEVICE=pdfwrite', '-dFastWebView', '-sOutputFile='+ bookpdfpath, collate_pdf]
ghostscript.Ghostscript(*ghostScriptExec)
delete = filepath + "collate.pdf"
os.remove(delete)
ghostScriptExec = ['gs', '-dPDFA', '-dBATCH', '-dNOPAUSE', '-dUseCIEColor', '-sProcessColorModel=DeviceRGB',
                   '-sDEVICE=pdfwrite', '-dFastWebView', '-sPDFACompatibilityPolicy=1',
                   '-sOutputFile='+ output_files + "/" + 'PDFA-' + "combined_pdf.pdf", bookpdfpath]
ghostscript.Ghostscript(*ghostScriptExec)


