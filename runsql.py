#run a sql string against the database and print the results
import dataset
db = dataset.connect('sqlite:///brahms.sqlite')
search = 'GZ 53'
sql = f'select * from specimens where fieldnumber REGEXP \'' + f'\\b{search}\\b' + '\''
res = db.query(sql)
for row in res:
  print(f'{row["Collector"]}: {row["FieldNumber"]}')