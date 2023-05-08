#drop -0 on barcodes for PRU database
import dataset
db = dataset.connect('sqlite:///brahms.sqlite')
table = db['specimens']

print('fixing barcodes...')
counter = 0
for row in table:
  barcode = row['Barcode']
  if '0' in barcode:
    barcode = barcode.split('-')[0]
    new_data = dict(id = row['id'], Barcode = barcode)
    table.update(new_data, ['id'])
    counter = counter + 1

db.close()
print(counter, 'barcodes updated...')