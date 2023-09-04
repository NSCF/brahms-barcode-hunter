#script to read the data from BRAHMS7 files and push to SQLite
#MAKE SURE YOU'VE ARCHIVED THE PREVIOUS DATABASE BEFORE YOU RUN THIS!!!
import dataset
import time
from progress.bar import Bar
from os import path
import csv

datafilepath = r'C:\Users\Ian Engelbrecht\Downloads'
datafile = r'Skukuza-BRAHMS-specimens-OpenRefine.csv'
countestimate = 16000

#SCRIPT

#first check if any previous database has been archived and removed
if path.exists('brahms.sqlite'):
  print('Please archive the current brahms.sqlite file and remove it from the root directory')
  exit()

#read all the data into sqlite
start = time.time()
db = dataset.connect('sqlite:///brahms.sqlite')
table = db['specimens'] #recreate

bar = Bar('', max = countestimate, suffix='%(percent)d%%')
with open(path.join(datafilepath, datafile), newline='', encoding='utf8') as csvfile:
  reader = csv.DictReader(csvfile)
  for row in reader:
    table.insert(row)
    bar.next()
bar.finish()

print('specimens columns:' , table.columns)

#add indexes
print('adding index')
table.create_index(['Accession', 'Collector', 'FieldNumber', 'CollectionDay', 'CollectionMonth', 'CollectionYear',
  'FamilyName', 'FullName', 'AcceptedName', 'Country', 'MajorAdmin', 'LocalityNotes'])

db.close()
end = time.time()

millis = end * 1000 - start * 1000
seconds = int((millis/1000)%60)
minutes = int((millis/(1000*60))%60)
hours = (millis/(1000*60*60))%24

print ("transfer completed in", "%d:%d:%d" % (hours, minutes, seconds))

print('all done')