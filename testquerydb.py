from querydb import querydb, get_countries, get_provinces

res = querydb({'fieldnumber': 'YBK 79'})
print('count is:', len(res))

# countries = get_provinces()
# i = 1
