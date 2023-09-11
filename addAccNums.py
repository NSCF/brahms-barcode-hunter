#the original Skukuza dataset came without accession numbers
#this script updates brahms.sqlite withthose accession numbers
from os import path
import csv
import dataset
from progress.bar import Bar
import re


csvDir = r'C:\temp\SkukuzaBRAHMS\csv'
csvFile = r'specimens.csv'
fileRows = 16000


db = dataset.connect('sqlite:///brahms.sqlite')
table = db['specimens']

print('updating data')
bar = Bar('Updating', max = fileRows, suffix='%(percent)d%%')
with open(path.join(csvDir, csvFile), 'r', newline='', errors='ignore') as f:
  reader = csv.DictReader(f)
  for row in reader:
    updateData = dict(Barcode=row['BARCODE'], Accession=re.sub('^0+', '', row['ACCESSION']))
    table.update(updateData, ['Barcode'])
    bar.next()
  
bar.finish()
print('all done')
