from os import walk

f = r"F:\Herbarium imaging\NU\Main Collection"
g = r"G:\Herbarium imaging\NU\Main Collection"

f_files = []
for (dirpath, dirnames, filenames) in walk(f):
    f_files.extend(filenames)

g_files = []
for (dirpath, dirnames, filenames) in walk(g):
    g_files.extend(filenames)

f_set = set(f_files)
g_set = set(g_files)

both = f_set.intersection(g_set)
print(len(both), 'files in both directories')