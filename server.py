import threading, webbrowser
from flask import Flask, request, current_app, make_response
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from printerInterface import wait_for_print_job_info, job_status_string
from querydb import querydb, get_countries, get_provinces, get_families

app = Flask(__name__, static_url_path='', static_folder='dist')
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

user_session_id = None

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

@socketio.on('connect')
def handle_connect():
  user_session_id = request.sid

@socketio.event
def my_event(message):
  emit('my response', {'data': 'got it!'})

def watchPrinter():
  t = threading.Timer(0.2, watchPrinter)
  t.daemon = True
  t.start()
  info = wait_for_print_job_info(timeout=0.25)
  if info:
    job_ids = []
    
    for nd in info:
      job_id, key, value = nd
      job_ids.append(job_id)
    
    socketio.emit('increment', {"job_ids": job_ids}, to=user_session_id)

watchPrinter()

if __name__ == '__main__':
  threading.Timer(1.25, lambda: webbrowser.open('http://127.0.0.1:5000') ).start()
  socketio.run(app, port=5000, debug=False)