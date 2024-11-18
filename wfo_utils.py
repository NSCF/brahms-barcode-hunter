import re

def make_fullname(wfo_record):
  ignore = ['subsp.', 'var.', 'subvar.', 'f.', 'subf.']
  name = wfo_record['scientificName']
  author = wfo_record['scientificNameAuthorship']

  if author:
    name_parts_reversed = name.split(' ')
    name_parts_reversed.reverse()
    last_name_part = ''
    last_name_part_index = 0
    for index, name_part in enumerate(name_parts_reversed):
      if name_part not in ignore:
        if name_part != last_name_part and last_name_part != '':
          break
        else:
          last_name_part = name_part
          last_name_part_index = index


    new_name_parts = [*name_parts_reversed[0:last_name_part_index], author, *name_parts_reversed[last_name_part_index:]]
    new_name_parts.reverse()
    name = ' '.join(new_name_parts)

  return name

def map_record(wfo_record):

  fullname = make_fullname(wfo_record)
    
  mapped = {
    "fullName": fullname,
    "author": wfo_record['scientificNameAuthorship'],
    "source" : "WFO",
    "identifier": wfo_record["taxonID"],
    "status": (wfo_record["taxonomicStatus"]).lower(),
  }

  return mapped

def get_parent_author(wfo_record, db):

  # we should only ever need to do this infraspecific taxa, so...
  while (wfo_record['scientificNameAuthorship'] is None):
    name_parts = wfo_record['scientificName'].split(' ')
    name_parts.pop() # drop the name
    name_parts.pop() # drop the infraspecific rank

    # safety catch
    if len(name_parts) <= 1: 
      return None
    
    search_name = ' '.join(name_parts)

    sql = 'select * from wfo_taxa where scientificName = :search and taxonomicStatus != \'deprecated\''
    results =  db.query(sql, search = search_name)
    result_count = 0
    for row in results:
      wfo_record = row
      result_count += 1

      # safety catch, in case we have multiple potential parents
      if result_count > 1:
        return None

  return wfo_record['scientificNameAuthorship']

def get_accepted_name(wfo_record, db):
  while (wfo_record['acceptedNameUsageID'] is not None):
    sql = 'select * from wfo_taxa where taxonID = :search'
    results =  db.query(sql, search = wfo_record['acceptedNameUsageID'])
    for row in results:
      wfo_record = row

  name = wfo_record['scientificName']
  if wfo_record['scientificNameAuthorship']:
    name += ' ' + wfo_record['scientificNameAuthorship']

  return name.strip()

def replace_specialchars(string):

  string = string.replace('Č', 'C')                 \
    .replace('Ç', 'C')                              \
    .replace('ç', 'c')                              \
    .replace('Ñ', 'N')                              \
    .replace('ñ', 'n')                              \
    .replace('Æ', 'AE')                             \
    .replace('æ', 'ae')                             \
    .replace('Œ', 'OE')                             \
    .replace('œ', 'oe')                             \
    .replace('Š', 'S')                              \
    .replace('š', 's')                              \
    .replace('Ž', 'Z')                              \
    .replace('ž', 'z')                              \
    .replace('Þ', 'Th')                             \
    .replace('ð', 'd')                              \
    .replace('ß', 'ss')                        
  
  string = re.sub(r'[áàâãäå]+', 'a', string)
  string = re.sub(r'[ÉÈÊË]+', 'E', string)
  string = re.sub(r'[éèêë]+', 'e', string)
  string = re.sub(r'[ÍÌÎÏ]+', 'I', string)
  string = re.sub(r'[íìîï]+', 'i', string)
  string = re.sub(r'[ÓÒÔÕÖØ]+', 'O', string)
  string = re.sub(r'[óòôõöø]+', 'o', string)
  string = re.sub(r'[ÚÙÛÜ]+', 'U', string)
  string = re.sub(r'[úùûü]+', 'u', string)
  string = re.sub(r'[ŁĹĻĽḶḺȽL̃]+', 'L', string)
  string = re.sub(r'[łĺļľḷḻƚl̃]+', 'l', string)
  string = re.sub(r'[ÝŶŸȲɎỲƳȜẎỴỾƔ]+', 'Y', string)
  string = re.sub(r'[ýŷÿȳɏỳƴȝẏỵỿƣ]+', 'y', string)

  return string