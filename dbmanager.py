# just for various sqlite management tasks, chop and change as needed

import dataset
db = dataset.connect('sqlite:///brahms.sqlite')
# for table in db.tables:
#   print(table)
table = db['taxa']
table.drop()
print('all done...')