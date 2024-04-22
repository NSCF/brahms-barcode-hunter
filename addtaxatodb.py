import dataset
import sys, time, re, csv
from progress.bar import Bar
from os import path

datafilepath = r'C:\Users\Ian Engelbrecht\Downloads'
datafile = r'SANBI-TaxonBackbone-Export-20231120-OpenRefine-withHigherClass-OpenRefine.csv'

dbfields = ['fullname', 'guid', 'status', 'acceptedname']

print('creating taxon table')
db = dataset.connect('sqlite:///taxa.sqlite')
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
      "fullname": re.sub(r'\s+', ' ', row["CalcFullName"]).strip(),
      "guid": row["GUID"],
      "status": row["TaxStatus"],
      "acceptedname": None
    }

    if re.sub(r'\s+', ' ', row["CalcFullName"]).strip() != re.sub(r'\s+', ' ', row["CalcAcceptedName"]).strip():
      data["acceptedname"] = re.sub(r'\s+', ' ', row["CalcAcceptedName"]).strip()

    table.insert(data)

    rowcount += 1

    if rowcount % 100 == 0:
      print(rowcount, 'records added', end='\r')


sys.stdout.write('\033[?25h') #resetting the console cursor
sys.stdout.flush()

end = time.perf_counter()
seconds = (end - start) % (24 * 3600)
hour = seconds // 3600
seconds %= 3600
minutes = seconds // 60
seconds %= 60
print(rowcount, "records added in", "%02dh:%02dm:%02ds" % (hour, minutes, seconds)) 

print('all done!')

