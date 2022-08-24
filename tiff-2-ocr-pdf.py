import sys
import os
import ocrmypdf
import ghostscript
from PyPDF2 import PdfFileMerger
import glob

print("\n TIFF to OCR PDF & PDF/A Conversion \n")
print("\n Date: 20 May 2022 \n\n")


'''
- Getting the Input file path from user
- creating the "PDF-A" directory for store the PDF/A output files
- language will be defined in "lang.ini" file in the same path of input files.
- language code should be three digit iso code, multiple language should be add by separation of "+" symbol. e.g.: eng+dan
- Tesseract version 5 should be installed in "C:\Program Files\Tesseract-OCR"
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
- Saved PDF file compression in png format, so the file size will be large
'''
for fname in os.listdir(filepath):
    if not fname.endswith(".tif"):
        continue
    input_file = os.path.join(filepath, fname) 
    pname = os.path.splitext(fname)[0]
    output_file = filepath + pname + ".pdf"
    f1 = open(output_file, "w+b")
    with open(langu) as f:   # open the ini file
        ini = f.read()       # read the ini file
    ocrmypdf.ocr(input_file, output_file, language=ini, force_ocr=True, output="pdf", jpeg_quality="100")
    f1.close()




# PDF files will changed to optimized format (JPEG compression) and fastweb view
# After changed to JPEG compression, the size of PDF file is normal actual size.
for fname in os.listdir(filepath):
    print(fname)
    if not fname.endswith(".pdf"):
        continue
    path = os.path.join(filepath, fname) 
    ghostScriptExec = ['gs', '-dBATCH', '-dNOPAUSE', '-dUseCIEColor', '-sProcessColorModel=DeviceRGB', '-dCompatibilityLevel=1.5', '-dJPEGQ=100', 
                   '-sDEVICE=pdfwrite', '-dFastWebView', '-dAutoRotatePages=/None', '-sOutputFile='+ filepath + 'Page-' + fname, path]
    ghostscript.Ghostscript(*ghostScriptExec)
    delete = filepath + fname
    os.remove(delete)
    print("\n Conversion Completed\n")



# PDF to PDF/A Conversion - PDF/A format "1b"
for fname in os.listdir(filepath):
    print(fname)
    if not fname.endswith(".pdf"):
        continue
    path = os.path.join(filepath, fname) 
    print(path)
    output_files = filepath + directory
    ghostScriptExec = ['gs', '-dPDFA', '-dBATCH', '-dNOPAUSE', '-dUseCIEColor', '-sProcessColorModel=DeviceRGB',
                   '-sDEVICE=pdfwrite', '-dFastWebView', '-dAutoRotatePages=/None', '-sPDFACompatibilityPolicy=1',
                   '-sOutputFile='+ output_files + "/" + 'PDFA-' + fname, path]
    ghostscript.Ghostscript(*ghostScriptExec)
    print("\n Conversion Completed\n")


# Book level PDF (Combined PDF) generation
# Book level PDF/A (Combined PDF) Conversion

collate_pdf = filepath + "/" + "collate.pdf"
bookpdfpath = filepath + "/" + "combined_pdf.pdf"
merger = PdfFileMerger()
for file in glob.glob(filepath + "*.pdf"): # glob module is used to match the files type
    merger.append(file)
merger.write(collate_pdf)
merger.close()

# collate_pdf file changed to fastwebview
ghostScriptExec = ['gs', '-dBATCH', '-dNOPAUSE', '-dUseCIEColor', '-sProcessColorModel=DeviceRGB', '-dCompatibilityLevel=1.5', '-dJPEGQ=100', 
                   '-sDEVICE=pdfwrite', '-dFastWebView', '-dAutoRotatePages=/None', '-sOutputFile='+ bookpdfpath, collate_pdf]
ghostscript.Ghostscript(*ghostScriptExec)
delete = filepath + "collate.pdf"
os.remove(delete)


ghostScriptExec = ['gs', '-dPDFA', '-dBATCH', '-dNOPAUSE', '-dUseCIEColor', '-sProcessColorModel=DeviceRGB',
                   '-sDEVICE=pdfwrite', '-dFastWebView', '-dAutoRotatePages=/None', '-sPDFACompatibilityPolicy=1',
                   '-sOutputFile='+ output_files + "/" + 'PDFA-' + "combined_pdf.pdf", bookpdfpath]
ghostscript.Ghostscript(*ghostScriptExec)


