#drop -0 on barcodes for PRU database
import dataset
db = dataset.connect('sqlite:///brahms.sqlite')
table = db['specimens']

print('fixing barcodes...')
counter = 0
for row in table:
  barcode = row['Barcode']
  if '-' in barcode:
    barcode = barcode.split(' ')[0]
    row['Barcode'] = barcode
    table.update(row, [id])
    counter = counter + 1

db.close()
print(counter, 'barcodes updated...')