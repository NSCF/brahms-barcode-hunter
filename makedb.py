#script read the data from BRAHMS7 files and push to SQLite
#MAKE SURE YOU'VE ARCHIVED THE PREVIOUS DATABASE BEFORE YOU RUN THIS!!!
import dataset
import time
from progress.bar import Bar
from os import path
import csv

datafile = r'PRU-BRAHMS-Extract-20230130-OpenRefine.csv'
countestimate = 60000

#SCRIPT

#read all the data into sqlite
start = time.time()
db = dataset.connect('sqlite:///brahms.sqlite')
tables = db.tables
if 'specimens' in tables:
  db['specimens'].drop() #drop previous imports
table = db['specimens'] #recreate


bar = Bar('', max = countestimate, suffix='%(percent)d%%')
with open(datafile, newline='', encoding='utf8') as csvfile:
  reader = csv.DictReader(csvfile)
  for row in reader:
    table.insert(row)
    bar.next()
bar.finish()

end = time.time()

millis = end * 1000 - start * 1000
seconds = int((millis/1000)%60)
minutes = int((millis/(1000*60))%60)
hours = (millis/(1000*60*60))%24

print ("transfer completed in", "%d:%d:%d" % (hours, minutes, seconds))

print('specimens columns:' , table.columns)

#add indexes
print('adding index')
table.create_index(['Accession', 'Collector', 'FieldNumber', 'CollectionDay', 'CollectionMonth', 'CollectionYear',
  'FamilyName', 'FullName', 'AcceptedName', 'Country', 'MajorAdmin', 'LocalityNotes'])

print('all done')