from querydb import querydb, get_countries, get_provinces

res = querydb({'accession': '0131081'})
print('count is:', len(res))

# countries = get_provinces()
# i = 1
