# import taxon records from the published SANBI plant checklist into a sqlite database
# make sure to remove all names with auct. before running this script

import dataset
import sys, time, re, csv
from progress.bar import Bar
from os import path

datafilepath = r'C:\Users\ianic\Downloads'
datafile = r'SA-Plant-Checklist-2024-OpenRefine.csv'
checklistdate = r'2024-03-20' # The ISO 8601 date that the checklist was published

dbfields = ['guid', 'fullname', 'status', 'acceptedname']

print('creating taxon table')
db = dataset.connect('sqlite:///taxa.sqlite')
table = db['taxa'] 
table.drop()
table = db['taxa'] #recreate

for field in dbfields:
  table.create_column(field, db.types.string)
table.create_index(['fullname'])

print('adding records to database')
sys.stdout.write('\033[?25l') #to clear the console cursor for printing progress
sys.stdout.flush()
start = time.perf_counter()
rowcount = 0
with open(path.join(datafilepath, datafile), newline='', encoding='utf8') as csvfile:
  reader = csv.DictReader(csvfile)
  for row in reader:
    data = {
      "guid": row["RecordGUID"],
      "fullname": re.sub(r'\s+', ' ', row["FullName"]).strip(),
      "status": row["TaxStatus"],
      "acceptedname": re.sub(r'\s+', ' ', row["AcceptedName"]).strip()
    }

    table.insert(data)

    rowcount += 1

    if rowcount % 100 == 0:
      print(rowcount, 'records added', end='\r')

sys.stdout.write('\033[?25h') #resetting the console cursor
sys.stdout.flush()

meta = db['meta'] 
if not meta.has_column('tablename'):
  meta.create_column('tablename', db.types.string)
if not meta.has_column('field'):
  meta.create_column('field', db.types.string)
if not meta.has_column('value'):
  meta.create_column('value', db.types.string)

data = dict(tablename='taxa', field="extractdate", value = checklistdate)
meta.upsert(data, ['tablename', 'field'])

db.close()

end = time.perf_counter()
seconds = (end - start) % (24 * 3600)
hour = seconds // 3600
seconds %= 3600
minutes = seconds // 60
seconds %= 60
print(rowcount, "records added in", "%02dh:%02dm:%02ds" % (hour, minutes, seconds)) 

print('all done!')

