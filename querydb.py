import dataset
db = dataset.connect('sqlite:///brahms.sqlite')

def querydb(searchparams):

  # #build the query
  sql = 'select * from specimens where'
  vals = {}

  searchterms = []

  if 'locality' in searchparams:
    searchterms.append('LocalityNotes like :locality')
    search = '%' + searchparams['locality'] + '%'
    vals['locality'] = search

  if 'collector' in searchparams:
    searchterms.append('collector like :collector')
    search = '%' + searchparams['collector'] + '%'
    vals['collector'] = search

  if 'accession' in searchparams:
    searchterms.append('accession = :accession')
    vals['accession'] = searchparams['accession']

  if 'fieldnumber' in searchparams:
    searchterms.append('fieldnumber like :fieldnumber')
    search = '%' + searchparams['fieldnumber'] + '%'
    vals['fieldnumber'] = search

  if 'day' in searchparams:
    searchterms.append('day = :day')
    vals['day'] = searchparams['day']

  if 'month' in searchparams:
    searchterms.append('month = :month')
    vals['month'] = searchparams['month']

  if 'year' in searchparams:
    searchterms.append('year = :year')
    vals['year'] = searchparams['year']

  if 'family' in searchparams:
    searchterms.append('family = :family')
    vals['family'] = searchparams['family']

  if 'country' in searchparams:
    searchterms.append('country = :country')
    vals['country'] = searchparams['country']

  if 'stateProv' in searchparams:
    searchterms.append('stateProv = :stateProv')
    vals['stateProv'] = searchparams['stateProv']

  if 'taxonname' in searchparams:
    searchterms.append('(fullname like :taxonname or acceptedname like :taxonname)')
    search = searchparams['taxonname'].replace(' ', '% ')
    search = search + '%'
    vals['taxonname'] = search

  results = []
  if len(vals) >= 2: #we need at least two search params
    allterms = ' and '.join(searchterms)
    sql += ' ' + allterms

    qry_results = db.query(sql, vals)
    
    for qry_result in qry_results:
      results.append(qry_result)
  else:
    raise Exception('at least two valid search params required')
  
  return results
