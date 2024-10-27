import dataset
import sys, time, re, csv
from progress.bar import Bar
from os import path

datafilepath = r'C:\Users\ianic\Downloads\WFO_Backbone'
datafile = r'classification.csv'
wfo_version = '2024.06'

dbfields = ['taxonID', 'family', 'scientificName', 'scientificNameAuthorship', 'taxonRank', 'taxonomicStatus', 'parentNameUsageID', 'acceptedNameUsageID', 'originalNameUsageID']

print('creating taxon table')
db = dataset.connect('sqlite:///wfo.sqlite')
table = db['wfo_taxa'] #recreate
for field in dbfields:
  table.create_column(field, db.types.string)

table.create_index(['taxonID'])
table.create_index(['family'])
table.create_index(['scientificName'])
table.create_index(['scientificNameAuthorship'])
table.create_index(['taxonRank'])
table.create_index(['taxonomicStatus'])
table.create_index(['parentNameUsageID'])
table.create_index(['acceptedNameUsageID'])
table.create_index(['originalNameUsageID'])


print('adding records to sqlite')
sys.stdout.write('\033[?25l') #to clear the console cursor for printing progress
sys.stdout.flush()
start = time.perf_counter()
rowcount = 0
with open(path.join(datafilepath, datafile), newline='', encoding='utf8', errors='ignore') as csvfile:
  reader = csv.DictReader(csvfile, delimiter="\t")
  for row in reader:
    data = { }
    for field in dbfields:
      if row[field] and row[field].strip():
        data[field] = re.sub("\s+", ' ', row[field]).strip() 
      else:
        row[field] = None

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

data = dict(tablename='taxa', field="version", value = wfo_version)
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

