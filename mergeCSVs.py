# merges a set of CSVs from a directory into one file, and includes the file names in the dataset. 
# note that all the CSVs have to have the same headers. Use checkCSVHeaders.py for that. 
# This is an alternative xsv (https://github.com/BurntSushi/xsv) where you want to include file names and avoid the mismatched field counts from xsv. 

import os
import csv

dir = r'D:\NSCF Data WG\Data\Herbaria\Bews Herbarium\Imaging project data capture\Individual spreadsheets'

headers = [
  'section',
  'station',
  'date',
  'order',
  'barcode', 
  'note', 
  'dwc:family', 
  'dwc:qualifier', 
  'dwc:scientificName', 
  'source', 
  'identifier', 
  'dwc:taxonomicStatus', 
  'acceptedName'
]

### SCRIPT ###

newfilename = "_all.csv"
if os.path.exists(os.path.join(dir, newfilename)):
  os.remove(os.path.join(dir, newfilename))

files = os.listdir(dir)
csvs = list(filter(lambda x: x.lower().endswith('.csv'), files))

try:
  with open(os.path.join(dir, newfilename), 'w', encoding='UTF8', newline='') as outfile:
    writer = csv.DictWriter(outfile, fieldnames= ['filename'] + headers)
    writer.writeheader()
    
    for csvFile in csvs:
      print('reading', csvFile)
      with open(os.path.join(dir, csvFile), 'r', encoding="UTF8", errors="ignore") as f:
        reader = csv.DictReader(f)
        first = next(reader)
        csvHeaders = list(first.keys())
        if headers != csvHeaders:
          raise Exception('headers in file ' + csvFile, ' don\'t match')
        
        first['filename'] = csvFile
        writer.writerow(first)
        while True:
          try:
            row = next(reader)
            row['filename'] = csvFile
            writer.writerow(row)
          except StopIteration:
            break

    print('all done...')

except Exception as ex:
  print(str(ex))