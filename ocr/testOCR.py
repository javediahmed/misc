# Test tesseract ocr file, convert pdf to image, process images

import pytesseract
from PIL import Image
import sys
from pdf2image import convert_from_path
import os
import io


DPI = 400

# Convert to a jpg, do ocr on the jpg, and print the results to a results_filename[0:20].txt
for pdf in os.listdir('pdfs'):
    pdf_path = 'pdfs/' + str(pdf)
    output_filename = "results_" + pdf_path.split('/')[-1].replace('.pdf','')[0:20] + ".txt"
    pages = convert_from_path(pdf_path, dpi=DPI)
    pg_cntr = 1
    sub_dir = str("images/" + pdf_path.split('/')[-1].replace('.pdf','')[0:20] + "/")
    if not os.path.exists(sub_dir):
        os.makedirs(sub_dir)

    for page in pages:
        filename = "pg_" + str(pg_cntr) + '_' + pdf_path.split('/')[-1].replace('.pdf', '.jpg')
        page.save(sub_dir+filename)
        with io.open(output_filename, 'a+', encoding='utf8') as f:
            f.write("----- START PAGE " + str(pg_cntr) + " -----\n")
            f.write(pytesseract.image_to_string(sub_dir+filename)+"\n")
            f.write("----- END PAGE " + str(pg_cntr) + " -----\n")
        pg_cntr += 1


