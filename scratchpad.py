import dataset

try:
    db = dataset.connect('sqlite:///asdf.sqlite', ensure_schema=False)
except Exception as ex:
    raise ex

pass