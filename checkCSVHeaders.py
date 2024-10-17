# Checks all csv files in a directory have a specific set of headers (case sensitive) and reports any that dont
import os
import csv

dir = r'C:\Herbarium imaging\NU\data'
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
files = os.listdir(dir)
csvs = list(filter(lambda x: x.lower().endswith('.csv'), files))

errorCount = 0
for csvFile in csvs:
  with open(os.path.join(dir, csvFile), 'r', encoding="UTF8", errors="ignore") as f:
    reader = csv.DictReader(f)
    first = next(reader)

    
    csvHeaders = list(first.keys())
    missing = list(set(headers) - set(csvHeaders))
    missing = list(filter(None, missing))
    additional = list(set(csvHeaders) - set(headers))
    additional = list(filter(None, additional))

    if len(missing) > 0:
      print(csvFile, 'missing:', ', '.join(missing))
      errorCount += 1
    if len(additional) > 0:
      print(csvFile, 'additional:', ', '.join(additional))
      errorCount += 1

    if '' in csvHeaders:
      print(csvFile, 'has blank columns')
      errorCount += 1
      csvHeaders = list(filter(None, csvHeaders))

    if len(missing) == 0 and len(additional) == 0:
      if headers != csvHeaders:
        print(csvFile, 'headers out of order')
        errorCount += 1

if errorCount == 0:
  print('All headers are correct, have a nice day...')


