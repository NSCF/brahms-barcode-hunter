from querydb import querydb

res = querydb({'locality': 'pella', 'taxonname': 'just gu'})
print('count is:', res)
