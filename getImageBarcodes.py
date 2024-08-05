# basically just getting the list of filenames of a particular file type from a particular location and saving to csv
# the outputs can then be merged and compared with the output of getSpreadsheetBarcodes
import re
import csv
import os

dir = r'D:\Herbarium imaging\NU\JPEG'
drive = "BEWS01"
file_ext = '.jpg'

print('reading', drive)
with open(drive + '.csv', 'w', encoding='UTF8', newline='') as f:
  writer = csv.writer(f)
  writer.writerow(['drive', 'location','barcode'])
  for (root,dirs,files) in os.walk(dir):
    for file in files:
      if file.lower().endswith(file_ext):
        location = root.replace(dir, '')
        barcode = re.split('[_-]', file)[0]
        barcode = re.sub(file_ext + '$', '', barcode, re.I)
        writer.writerow([drive, location, barcode])

print('all done...')





