from querydb import querydb, get_countries, get_provinces, get_BODATSA_names, get_WFO_names
import json

# res = querydb({'fieldnumber': 'YBK 79'})
# print('count is:', len(res))

# countries = get_provinces()
# i = 1

# names = get_WFO_names("care vulp")
# i = 1

names = get_BODATSA_names("strel reg")
json_names = json.dumps(names)
i = 1