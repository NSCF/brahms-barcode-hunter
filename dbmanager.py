# just for various sqlite management tasks, chop and change as needed

import dataset
db = dataset.connect('sqlite:///taxa.sqlite')
for table in db.tables:
  print(table)
# table = db['taxa']
# table.drop()

# extractdate = r'2023-11-20' # ISO8601 format date of the BRAHMS extract used
# meta = db['meta'] 
# if not meta.has_column('tablename'):
#   meta.create_column('tablename', db.types.string)
# if not meta.has_column('field'):
#   meta.create_column('field', db.types.string)
# if not meta.has_column('value'):
#   meta.create_column('value', db.types.string)

# data = dict(tablename='taxa', field="extractdate", value = extractdate)
# meta.upsert(data, ['tablename', 'field'])

print('all done...')