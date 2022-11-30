from flask import Flask, request, current_app
from querydb import querydb

app = Flask(__name__, static_url_path='', static_folder='dist')

@app.route('/', methods=['GET'])
def home():
  if request.method == 'GET':
    return current_app.send_static_file('index.html')

@app.route('/search', methods = ["GET"])
def search():
  if request.method == 'GET':
    if len(request.args):
      try:
        results = querydb(request.args)
        return results
      except Exception as e:
        return str(e)
    else:
      return 'query paramters are required'

  else:
    return 'invalid call method'

if __name__ == '__main__':
  app.debug = True
  app.run()