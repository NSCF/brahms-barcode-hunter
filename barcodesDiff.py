#Check which barcodes in a file are not on the database
import csv
from  os import path
import dataset
from progress.bar import Bar

#csv file with a field called 'barcode'
csvPath = r'F:\Herbarium imaging\PRU\processing'
csvFileName = r'20230508 - barcodes.csv'

barcodes = set() #we need the unique values
with open(path.join(csvPath, csvFileName), newline='') as csvfile:
  reader = csv.DictReader(csvfile)
  for row in reader:
    barcodes.add(row['barcode'])

print(len(barcodes), 'unique barcodes in', csvFileName)

#get barcodes not in db
print('checking against database')
bar = Bar('', max = len(barcodes), suffix='%(percent)d%%')
new_barcodes = []
db = dataset.connect('sqlite:///brahms.sqlite')
specimens = db['specimens']
for barcode in barcodes:
  result = specimens.count(Barcode=barcode)
  if result == 0:
    new_barcodes.append(barcode)

  bar.next()

bar.finish()

db.close()


if len(new_barcodes) > 0:

  print(len(new_barcodes), 'are not in the database. Writing to file...')

  new_barcodes.sort()

  with open('not_captured.csv', 'w', newline='') as csvfile:
    fieldnames = ['barcode']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()

    for barcode in new_barcodes:
      writer.writerow({'barcode': barcode})

else:
  print('all barcodes are in the database...')

print('all done...')
