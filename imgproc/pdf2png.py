"""
Script: pdf2png.py
Desc:   Extract all pages to png from the pdf file
        and convert them to black-and-white image   
Usage:  pdf2png.py /PDF/DIRECTORY/PATH PDFNAME.pdf
"""
#!/usr/bin/env python3

import os, sys
import cv2 as cv
import numpy as np
from pdf2image import convert_from_path, pdfinfo_from_path

IMGPATH = 'directory/path/to/your/pdf'
PDF = 'file.pdf'

if len(sys.argv) != 3:
  print("Usage: ")
  print(sys.argv[0] + " /PDF/DIRECTORY/PATH PDFNAME.pdf")
  exit(0)
else:
  len(sys.argv) == 3:
  IMGPATH = sys.argv[1]
  PDF = sys.argv[2]


def gaussian_thresholding(img_path: str):
  img = cv.imread(img_path, cv.IMREAD_GRAYSCALE)
  assert img is not None, "file could not be read, check with os.path.exists()"
  #img = cv.medianBlur(img,5)
  img = cv.GaussianBlur(img,(5,5),0)
  th = cv.adaptiveThreshold(img, 255, \
              cv.ADAPTIVE_THRESH_GAUSSIAN_C,\
              cv.THRESH_BINARY,11,2)
  return th

def otsu_thresholding(img_path: str):
  img = cv.imread(img_path, cv.IMREAD_GRAYSCALE)
  assert img is not None, "file could not be read, check with os.path.exists()"
  blur = cv.GaussianBlur(img,(5,5),0)
  ret,th = cv.threshold(blur,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)
  return th

pdf_path = os.path.join(IMGPATH, PDF)
pdf_info = pdfinfo_from_path(pdf_path)
OUTFOLDER = os.path.join(IMGPATH, 'out')
TOTAL_PAGES = pdf_info['Pages']

os.makedirs(OUTFOLDER, exist_ok=True)
for i in range(1,TOTAL_PAGES+1):
  print(f"Processing page {i}")
  pages = convert_from_path(pdf_path, dpi=400, fmt="png", first_page=i, last_page=i)
  for page in pages:
    image_path = os.path.join(OUTFOLDER, f"page_{i}.png")
    page.save(image_path, "PNG")
    
    im_bin = gaussian_thresholding(image_path)
    cv.imwrite(im_bin, os.path.join(OUTFOLDER, f"gau_bw_page_{i}.png"))
    im_bin = otsu_thresholding(image_path)
    cv.imwrite(im_bin, os.path.join(OUTFOLDER, f"otsu_bw_page_{i}.png"))
    print(f"Page {i} saved")
