import dataset
db = dataset.connect('sqlite:///pre.sqlite')
tables = db.tables
i = 1