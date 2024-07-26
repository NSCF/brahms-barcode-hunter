# basically just getting the list of filenames of a particular file type from a particular location and saving to csv
# the outputs can then be merged and compared with the output of 
import re
import csv
import os

dir = r'T:\Herbarium imaging\NU'
drive = "NSCF30"

print('reading', drive)
with open(drive + '.csv', 'w', encoding='UTF8', newline='') as f:
  writer = csv.writer(f)
  writer.writerow(['drive', 'location','barcode'])
  for (root,dirs,files) in os.walk(dir):
    for file in files:
      if file.lower().endswith('.jpg'):
        location = root.replace(dir, '')
        barcode = re.split('[_-]', file)[0]
        barcode = re.sub('.jpg$', '', barcode, re.I)
        writer.writerow([drive, location, barcode])

print('all done...')





