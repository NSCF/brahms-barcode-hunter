# read image metadata directly from the lrcat file
# make sure to do this on a copy of the working lrcat file so you don't accidentally corrupt it. 
# see https://www.dpreview.com/forums/thread/4358462 for SQL examples and clues to the table structure

from os import path
import sqlite3
import csv

lrcat_dir = r"C:\Users\ianic\OneDrive\Pictures\Lightroom\NU Herbarium Catalogue"
lrcat_file = r"NU-v13-3.lrcat"
outfile = 'lrcat_nu.csv'

def dict_factory(cursor, row):
  d = {}
  for idx, col in enumerate(cursor.description):
    d[col[0]] = row[idx]
  return d

conn = sqlite3.connect(path.join(lrcat_dir, lrcat_file))
conn.row_factory = dict_factory
cursor = conn.cursor()


# I need file name, date, station, and possibly the timestamp
# AgHarvestedIptcMetadata has day month and year as floats
# AgInternedExifCameraSN
qry = """ 
  SELECT AgLibraryFile.basename as file, AgLibraryFile.extension as type, AgInternedExifCameraSN.value as camera, Adobe_images.captureTime as CaptureTime 
  FROM AgLibraryFile
  LEFT JOIN Adobe_images ON AgLibraryFile.id_local=Adobe_images.rootFile
  LEFT JOIN AgHarvestedExifMetadata ON AgHarvestedExifMetadata.image = Adobe_images.id_local
  LEFT JOIN AgInternedExifLens ON AgInternedExifLens.id_local = AgHarvestedExifMetadata.lensRef
  LEFT JOIN AgInternedExifCameraSN on AgInternedExifCameraSN.id_local = AgHarvestedExifMetadata.cameraSNRef;
"""

cursor.execute(qry)
# records = cursor.fetchall()

print('writing data to file, this might take a few minutes...')

with open(outfile, 'w', newline='', errors='ignore') as f: 
  writer = csv.writer(f)
  row = cursor.fetchone()
  writer.writerow(row.keys())
  writer.writerow(row.values())
  row = cursor.fetchone()
  while row:
    writer.writerow(row.values())
    row = cursor.fetchone()
  
conn.close()
print('all done')

