import dataset
import csv

db = dataset.connect('sqlite:///brahms.sqlite')
table = db['specimens']

with open('PRU-db-records.csv', 'w', newline='') as f:
  writer = csv.DictWriter(f, cols)
  writer.writeheader()
  for row in table:
    writer.writerow(row)

print('all done')