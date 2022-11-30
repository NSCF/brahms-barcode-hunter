#script read the data from BRAHMS7 files and push to MySQL
import dataset
import time
from progress.bar import Bar
from os import path
import csv

datafile = r'PRE_Specimens_Export20221128_111127.csv'
countestimate = 1100000

#SCRIPT

#read all the data into sqlite
start = time.time()
db = dataset.connect('sqlite:///brahms.sqlite')
#db['specimens'].drop() #drop previous imports
table = db['specimens']


# bar = Bar('', max = countestimate, suffix='%(percent)d%%')
# with open(datafile, newline='') as csvfile:
#   reader = csv.DictReader(csvfile)
#   for row in reader:
#     table.insert(row)
#     bar.next()
# bar.finish()

# end = time.time()

# millis = end * 1000 - start * 1000
# seconds = int((millis/1000)%60)
# minutes = int((millis/(1000*60))%60)
# hours = (millis/(1000*60*60))%24

# print ("transfer completed in", "%d:%d:%d" % (hours, minutes, seconds))

#add indexes
print('specimens columns:' , table.columns)

# print('adding index')
# table.create_index(['Accession', 'Collector', 'FieldNumber', 'CollectionDay', 'CollectionMonth', 'CollectionYear',
#   'FamilyName', 'FullName', 'AcceptedName', 'Country', 'MajorAdmin', 'LocalityNotes'])

print('all done')

# species_records = DBF(path.join(brahms_file_path, 'SPECIES.DBF'))
# for species in species_records:
#   print(species)
#   exit()

# specimen_records = DBF(path.join(brahms_file_path, 'SPECIMENS.DBF'))
# total = len(specimen_records)
# print(total, 'specimen records in BRAHMS')


# mydb = mysql.connector.connect(
#   host=dbhost,
#   user=dbadmin,
#   password=dbadminpassword,
#   database=dbname
# )

# createdbsql = 'CREATE SCHEMA brahms_barcodes IF NOT EXISTS'

# droptblsql = 'DROP TABLE brahms_barcodes IF EXISTS'

# createtblsql = '''CREATE TABLE `records` IF NOT EXISTS (
#   `barcode` varchar(20) NOT NULL,
#   `fullname` varchar(200) DEFAULT NULL,
#   `acceptedname` varchar(200) DEFAULT NULL,
#   `accession` varchar(45) DEFAULT NULL,
#   `collector` varchar(45) DEFAULT NULL,
#   `collectornum` varchar(15) DEFAULT NULL,
#   `locality` varchar(500) DEFAULT NULL,
#   `year` int(11) DEFAULT NULL,
#   `month` int(11) DEFAULT NULL,
#   `day` int(11) DEFAULT NULL,
#   `localitymetaphone` varchar(45) DEFAULT NULL,
#   UNIQUE KEY `barcode_UNIQUE` (`barcode`),
#   KEY `fullname` (`fullname`),
#   KEY `acceptedname` (`acceptedname`),
#   KEY `accession` (`accession`),
#   KEY `collector` (`collector`),
#   KEY `collectornum` (`collectornum`),
#   KEY `locality` (`locality`),
#   KEY `year` (`year`),
#   KEY `month` (`month`),
#   KEY `day` (`day`),
#   KEY `localitymetaphone` (`localitymetaphone`)
# ) ENGINE=InnoDB DEFAULT CHARSET=latin1;
# '''


