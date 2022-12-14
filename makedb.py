#script read the data from BRAHMS7 files and push to MySQL
import dataset
import time
from progress.bar import Bar
from os import path
import csv

datafile = r'PRE_Specimens_Export20221128_111127.csv'
countestimate = 900000

#SCRIPT

#read all the data into sqlite
start = time.time()
db = dataset.connect('sqlite:///brahms.sqlite')
#db['specimens'].drop() #drop previous imports
table = db['specimens']


bar = Bar('', max = countestimate, suffix='%(percent)d%%')
with open(datafile, newline='') as csvfile:
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