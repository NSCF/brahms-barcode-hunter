# A place for miscellaneous code...

import dataset
import csv

db = dataset.connect('sqlite:///brahms.sqlite')

sql = 'select * from specimens where fullname like \'%barleria%\''
qry = db.query(sql)
results = []
for row in qry:
    results.append({
        "barcode": row['Barcode'], 
        "family": row['FamilyName'], 
        "fullname": row['FullName']
    })
db.close()
db = None

with open('temprecords.csv', 'w', newline='') as csvfile:
    fieldnames = results[0].keys()
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()

    for result in results:
        writer.writerow(result)