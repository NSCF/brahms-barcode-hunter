#counts the total and unique barcodes across a set of csv files
import csv
import os

csvpath = r'C:\Users\i.vandermerwe\Downloads\barcode_csvs'

total = []
uniques = set()

files = os.listdir(csvpath)

print('reading files')
for file in files:
  with open(os.path.join(csvpath, file), newline='', errors='ignore') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
      barcode = row['barcode'].strip()
      if barcode != '':
        total.append(barcode)
        uniques.add(barcode)

print(len(total), 'total barcodes')
print(len(uniques), 'unique barcodes')
print('ratio is', len(total) / len(uniques))



