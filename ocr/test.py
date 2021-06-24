# Test tesseract ocr file, convert pdf to image, process images
import pytesseract
from PIL import Image
import sys
from pdf2image import convert_from_path
import os
import io

DPI = 400
FILEPATH = 'path/to/pdf'
OUTPUT_DIR = '.'
OUTPUTS = iter(('outfile1', 'outfile2'))

if len(sys.argv) > 1:
    FILEPATH = sys.argv[1]

def read_pdf(pdf_path, output_dir=OUTPUT_DIR, outputs=OUTPUTS, dpi=DPI):
    pages = convert_from_path(pdf_path, dpi=dpi)
    for page in pages:
        print(type(page))
        pg_cntr = 1
        filename_output = "pg_" + str(pg_cntr) + '_' + pdf_path.split('/')[-1].replace('.pdf', '.jpg')
        # filename_output = output_dir + next(outputs)
        page.save(filename_output)
        with io.open(filename_output, 'a+', encoding='utf8') as f:
            f.write("----- START PAGE " + str(pg_cntr) + " -----\n")
            f.write(pytesseract.image_to_string(output_dir + next(outputs))+"\n")
            f.write("----- END PAGE " + str(pg_cntr) + " -----\n")
        pg_cntr += 1

if __name__=='__main__':
    read_pdf(FILEPATH)
