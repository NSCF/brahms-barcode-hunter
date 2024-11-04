from urllib.parse import unquote
import threading, webbrowser, requests, re
from flask import Flask, abort, request, current_app, make_response, render_template, jsonify
from flask_caching import Cache
from flask_cors import CORS
from flask_socketio import SocketIO
from printerInterface import wait_for_print_job
from querydb import querydb, get_countries, get_provinces, get_families, get_WFO_names, get_BODATSA_names, get_BODATSA_extractdate, get_WFO_by_ID, get_WFO_canonical

cache = Cache(config={ 'CACHE_TYPE': 'SimpleCache' })
app = Flask(__name__, static_url_path='', static_folder='dist')
cache.init_app(app)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

user_session_id = None
user_session_status = None
print_count = 0

@app.route('/', methods=['GET'])
def home():
  if request.method == 'GET':
    return current_app.send_static_file('index.html')
  
#for getting print counts directly
@app.route('/count', methods=['GET'])
def count():
  return render_template('count.html', 
                         session_id=user_session_id,
                         session_status=user_session_status,
                         print_count=print_count)

@app.route('/search', methods = ["GET"])
def search():
  if request.method == 'GET':
    if len(request.args):
      try:
        results = querydb(request.args)
        return results
      except Exception as e:
        return make_response(str(e), 400)
    else:
      return make_response('query paramters are required', 400)
  else:
    return make_response('invalid call method', 400)

@app.route('/countries', methods = ["GET"])
def countries():
  return get_countries()

@app.route('/provinces', methods = ["GET"])
def provinces():
  return get_provinces()

@app.route('/families', methods = ["GET"])
def families():
  return get_families()

@app.route('/namesearch', methods=["GET"])
@cache.cached(timeout=36000, query_string=True)
def name_search():
    
    if 'source' not in request.args:
      return ('source is required', 400)
    
    if request.args['source'] not in ['WFO', 'SANBI']:
      return('source must be one of WFO or SANBI')
    
    if 'search_string' not in request.args:
      return ('no search string parameter', 400)
    
    if not request.args['search_string'] or not request.args['search_string'].strip():
      return ('no search string provided', 400)
    
    source = request.args['source']   
    search_string = request.args['search_string']

    if source == 'WFO':
      try:
        results = get_WFO_names(search_string)
        return results
      except Exception as ex:
        return(str(ex), 500)
      
    if source == 'SANBI':
      results = get_BODATSA_names(search_string)
      return results

@app.route('/wfoname/<wfo_id>', methods=["GET"])
@cache.cached(timeout=36000, query_string=True)
def get_wfo_name(wfo_id):
    
    if not wfo_id:
      return ('wfo id is required', 400)
  
    try:
      result = get_WFO_by_ID(wfo_id)
      if not result:
        abort(404)
      else:
        return result
    except Exception as ex:
      return (str(ex), 500)
    

@app.route('/wfocanonical/<canonical_name>', methods=["GET"])
def get_wfo_canonical_name(canonical_name):
  
  if not canonical_name or not canonical_name.strip():
    return ('wfo id is required', 400)
  
  try:
    result = get_WFO_canonical(unquote(canonical_name.strip().replace('+', ' ')))
    if not result:
      abort(404)
    else:
      return result
  except Exception as ex:
      return (str(ex), 500)

@app.route('/bodatsaextractdate', methods=["GET"])
def fetch_date():
  return get_BODATSA_extractdate()


@socketio.on('connect')
def handle_connect():
  global user_session_id
  global user_session_status
  user_session_id = request.sid
  user_session_status = 'connected'

def watchPrinter():
  global print_count
  global user_session_id
  try:
    while True:
      info = wait_for_print_job()
      if not info:
        continue
      print_count += 1 
      socketio.emit('increment', to=user_session_id)
  except KeyboardInterrupt:
    return    

thread = threading.Thread(target=watchPrinter)
thread.daemon = True
thread.start()

if __name__ == '__main__':
  threading.Timer(1.25, lambda: webbrowser.open('http://127.0.0.1:5000') ).start()
  socketio.run(app, port=5000, debug=False)