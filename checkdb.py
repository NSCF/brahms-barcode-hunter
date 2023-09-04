import dataset
db = dataset.connect('sqlite:///brahms.sqlite')
tables = db.tables

print('Row counts:')
for table in tables:
  sql = f'select count(*) as cnt from {table}'
  res = db.query(sql)
  for row in res:
    print(f'{table}: {row["cnt"]}')

db.close()