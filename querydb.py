from os import path
import re
import dataset, requests

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

def get_WFO_names(search_string):
  if search_string and search_string.strip():

    search_string = re.sub(r'\s+', '* ', search_string)

    url = 'https://list.worldfloraonline.org/gql.php'
    headers = {
      'Content-Type': 'application/json',
    }

    query = '''
      query GetTaxa($searchString: String!) {
        taxonNameSuggestion(termsString: $searchString) {
          fullNameStringPlain,
          id,
          role,
          currentPreferredUsage {
            hasName {
              fullNameStringPlain,
              authorsString
            }
          }
        }
      }
    '''

    data = {'query': query, 'variables': {'searchString': search_string}}
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        results = response.json()
        data = results["data"]["taxonNameSuggestion"]
        #we need to add the source
        all_mapped = []
        for record in data:
          mapped = {
            "fullName": record["fullNameStringPlain"],
            "source" : "WFO",
            "identifier": record["id"],
            "status": record["role"],
            "acceptedName": '-'
          }

          if record["currentPreferredUsage"] and record["currentPreferredUsage"]["hasName"] and record["currentPreferredUsage"]["hasName"]["fullNameStringPlain"]:
            accepted_name = record["currentPreferredUsage"]["hasName"]["fullNameStringPlain"]
            if mapped["fullName"] != accepted_name:
              mapped["acceptedName"] = accepted_name

          all_mapped.append(mapped)

        sorted_mapped = sorted(all_mapped, key=lambda d: d['fullName'])
        return sorted_mapped
    
    else:
        return (response.text, response.status_code)
  else:
    raise Exception('search string is required')
  
def get_BODATSA_names(search_string):
  
  db = dataset.connect('sqlite:///taxa.sqlite')

  search_string = re.sub(r'\s+', '% ', search_string + ' ').strip() # adding the space on the end so we get the extra %
  sql = "select * from taxa where fullname like :search"
  query_results = []
  for row in db.query(sql, search = search_string):
    mapped = {
      "fullName": row["fullname"],
      "source" : "SANBI",
      "identifier": row["guid"],
      "status": row["status"],
      "acceptedName": row['acceptedname'] # this is already empty if the same as fullname
    }

    if mapped['acceptedName'] is None or mapped['acceptedName'] == '':
      mapped['acceptedName'] = "-"
      
    query_results.append(mapped)

  sorted_results = sorted(query_results, key=lambda d: d['fullName'])
  return sorted_results
  
def get_BODATSA_extractdate():
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
      
