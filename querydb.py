from os import path
import re
import dataset, requests
from wfo_utils import map_record, get_parent_author, get_accepted_name

def querydb(searchparams):

  db = dataset.connect('sqlite:///brahms.sqlite')

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
    searchterms.append('fieldnumber REGEXP \'' + f'\\b{searchparams["fieldnumber"]}\\b' + '\'') #match whole numbers in string
    search = '%' + searchparams['fieldnumber']
    vals['fieldnumber'] = search

  if 'day' in searchparams:
    searchterms.append('collectionday = :day')
    vals['day'] = searchparams['day']

  if 'month' in searchparams:
    searchterms.append('collectionmonth = :month')
    vals['month'] = searchparams['month']

  if 'year' in searchparams:
    searchterms.append('collectionyear = :year')
    vals['year'] = searchparams['year']

  if 'family' in searchparams:
    searchterms.append('familyname = :family')
    vals['family'] = searchparams['family']

  if 'country' in searchparams:
    searchterms.append('country = :country')
    vals['country'] = searchparams['country']

  if 'stateProv' in searchparams:
    searchterms.append('majoradmin = :stateProv')
    vals['stateProv'] = searchparams['stateProv']

  if 'taxonname' in searchparams:
    searchterms.append('(fullname like :taxonname or acceptedname like :taxonname)')
    search = searchparams['taxonname'].replace(' ', '% ')
    search = search + '%'
    vals['taxonname'] = search

  results = []
  allterms = ' and '.join(searchterms)
  sql += ' ' + allterms

  print(sql)
  qry_results = db.query(sql, vals)
  
  for qry_result in qry_results:
    results.append(qry_result)
  
  db.close()
  return results

def get_countries():
  db = dataset.connect('sqlite:///brahms.sqlite')
  sql = 'select distinct country from specimens'
  qry = db.query(sql)
  results = []
  for row in qry:
    results.append(row['Country'])
  db.close()
  return results

def get_provinces():
  db = dataset.connect('sqlite:///brahms.sqlite')
  sql = 'select distinct majoradmin from specimens where country = \'South Africa\''
  qry = db.query(sql)
  results = []
  for row in qry:
    results.append(row['MajorAdmin'])
  db.close()
  return results

def get_families():
  db = dataset.connect('sqlite:///brahms.sqlite')
  sql = 'select distinct familyname from specimens'
  qry = db.query(sql)
  results = []
  for row in qry:
    results.append(row['FamilyName'])
  db.close()
  return results

def get_WFO_by_ID(wfo_id):

  if wfo_id and wfo_id.strip() and re.match("wfo\-\d{10}", wfo_id):

    db = dataset.connect('sqlite:///wfo.sqlite')
    sql = "select * from wfo_taxa where taxonID = :wfo_id"
    results = []
    for row in db.query(sql, wfo_id = wfo_id):

      if row['scientificNameAuthorship'] is None:
        row['scientificNameAuthorship'] = get_parent_author(row, db)

      mapped = map_record(row)
      mapped['acceptedName'] = get_accepted_name(row, db)
        
      results.append(mapped)

    db.close()

    if results:
      return results[0] # there should only be one
    else:
      return None
    
  else:
    raise Exception('invalid wfo_id')

# TODO move back to the WFO API if they fix the issue with searches with multiple name parts https://github.com/rogerhyam/wfo-plant-list/issues/11
def get_WFO_names(search_string):
  if search_string and search_string.strip():

    db = dataset.connect('sqlite:///wfo.sqlite')

    search_string = re.sub(r'\s+', '% ', search_string + ' ').strip() # adding the space on the end so we get the extra %
    sql = "select * from wfo_taxa where scientificName like :search and taxonomicStatus != \'deprecated\'"
    query_results = []
    for row in db.query(sql, search = search_string):

      if row['scientificNameAuthorship'] is None:
        row['scientificNameAuthorship'] = get_parent_author(row, db)

      # if author is still None then it means there are multiple taxa with the parent name, 
      # and we can't actually be sure which infraspecific taxon we're dealing with,
      # so we don't want to return it as an option
      if not row['scientificNameAuthorship']:
        continue

      mapped = map_record(row)
      mapped['acceptedName'] = get_accepted_name(row, db)

      query_results.append(mapped)

    sorted_results = sorted(query_results, key=lambda d: d['fullName'])
    db.close()

    return sorted_results
  
  else:
    raise Exception('search string is required')

def get_WFO_canonical(canonical_name):

  if canonical_name and canonical_name.strip():

    db = dataset.connect('sqlite:///wfo.sqlite')
    sql = "select * from wfo_taxa where scientificName like :canonical"
    results = []
    for row in db.query(sql, canonical = canonical_name.strip()+'%'):

      if row['scientificNameAuthorship'] is None:
        row['scientificNameAuthorship'] = get_parent_author(row, db)

      mapped = map_record(row)
      mapped['acceptedName'] = get_accepted_name(row, db)
        
      results.append(mapped)

    db.close()

    if results:
      return results
    else:
      return None
    
  else:
    raise Exception('invalid canonical name')

def get_BODATSA_names(search_string):
  
  db = dataset.connect('sqlite:///taxa.sqlite')

  search_string = re.sub(r'\s+', '% ', search_string + ' ').strip() # adding the space on the end so we get the extra %
  sql = "select * from taxa where fullname like :search"
  query_results = []
  for row in db.query(sql, search = search_string):

    #remove auct. names
    if 'auct.' in row['fullname']: 
      continue;
      
    mapped = {
      "fullName": row["fullname"],
      "source" : "SANBI",
      "identifier": row["guid"],
      "status": row["status"],
      "acceptedName": row['acceptedname'] # this is already empty if the same as fullname
    }
      
    query_results.append(mapped)

  db.close()
  sorted_results = sorted(query_results, key=lambda d: d['fullName'])
  return sorted_results
  
def get_checklist_date():
  if path.exists('taxa.sqlite'):
    db = dataset.connect('sqlite:///taxa.sqlite')
    if db.has_table('taxa'):
      sql = "select * from meta where tablename = 'taxa' and field = 'extractdate'"
      result = []
      for row in db.query(sql):
        result.append(row)
      return result
    return []
  return []

def get_WFO_date():
  if path.exists('wfo.sqlite'):
    db = dataset.connect('sqlite:///wfo.sqlite')
    if db.has_table('wfo_taxa'):
      sql = "select * from meta where tablename = 'taxa' and field = 'version' order by value desc limit 1"
      result = []
      for row in db.query(sql):
        result.append(row)
      return result
    return []
  return []
      
