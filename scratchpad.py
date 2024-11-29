import csv, re
from os import path

csvDir = r'C:\Users\ianic\Downloads'
csvFile = r'SANBI-TaxonBackbone-Export-20240823-OpenRefine-SpecialCharAuthors.csv'
specialChars = list('ÁÀÂÃÄáàâãäÉÈÊËéèêëÍÌÎÏíìîïÓÒÔÕÖóòôõöÚÙÛÜúùûüČÇçÑñØøÆæŒœŠšŽžÅåÞðßØœ')

name_set = set()
with open(path.join(csvDir, csvFile), 'r', newline='', errors='ignore', encoding='utf8') as f:
  reader = csv.DictReader(f)
  for row in reader:
    authors = row['WfoidAuthor'].replace('(', '')
    author_list = re.split(r"[,)&]|ex", authors)
    for author in author_list:
      if bool(re.search(r"[^\x00-\x7F]", author)):
        name_set.add(author.strip())

name_set = list(name_set)
name_set.sort()

for name in name_set:
  print(name)
