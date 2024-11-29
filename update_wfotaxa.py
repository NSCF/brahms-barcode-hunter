import dataset
import sys, time, re, csv
from os import path
from wfo_utils import replace_specialchars

datafilepath = r'C:\Users\ianic\Downloads\WFO_Backbone'
datafile = r'classification.csv'

print('adding new field for each record')

sys.stdout.write('\033[?25l') #to clear the console cursor for printing progress
sys.stdout.flush()
start = time.perf_counter()
rowcount = 0

db = dataset.connect('sqlite:///wfo.sqlite')
table = db['wfo_taxa'] 
for row in table:
  
  row_scientific_name = row['scientificName']
  row_author = row['scientificNameAuthorship']
  if not row_author:
    row_author = ''

  homogenized_name = replace_specialchars(row_scientific_name + row_author).lower().replace(' ', '')  
  
  update_data = dict(taxonID = row['taxonID'], homogenizedName=homogenized_name)
  table.update(update_data, ['taxonID'])

  rowcount += 1

  if rowcount % 100 == 0:
    print(rowcount, 'records updated', end='\r')

sys.stdout.write('\033[?25h') #resetting the console cursor
sys.stdout.flush()

print('all records processed')
print('creating new index')
table.create_index(['homogenizedName']) #this is the standardized form of the name, to aid matches and searching for duplicates
db.close()

end = time.perf_counter()
seconds = (end - start) % (24 * 3600)
hour = seconds // 3600
seconds %= 3600
minutes = seconds // 60
seconds %= 60
print(rowcount, "records updated in", "%02dh:%02dm:%02ds" % (hour, minutes, seconds)) 
