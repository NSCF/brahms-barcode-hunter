import dataset
db = dataset.connect('sqlite:///brahms.sqlite')
tables = db.tables
print(tables)
db.close()