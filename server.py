import threading, webbrowser
from flask import Flask, request, current_app, make_response, render_template
from flask_cors import CORS
from flask_socketio import SocketIO
from printerInterface import wait_for_print_job_info, job_status_string
from querydb import querydb, get_countries, get_provinces, get_families

app = Flask(__name__, static_url_path='', static_folder='dist')
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

user_session_id = None
user_session_status = None
print_ids = set() #to track the print count

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
                         print_count=len(print_ids))


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
  global user_session_id
  global user_session_status
  user_session_id = request.sid
  user_session_status = 'connected'

def watchPrinter():
  t = threading.Timer(0.2, watchPrinter)
  t.daemon = True
  t.start()
  info = wait_for_print_job_info(timeout=0.1)
  if info:
    job_ids = []
    for nd in info:
      job_id, key, value = nd
      job_ids.append(job_id)
      print_ids.add(job_id)
    
    print('sending increment message to', user_session_id)
    socketio.emit('increment', {"job_ids": job_ids}, to=user_session_id)

watchPrinter()

if __name__ == '__main__':
  threading.Timer(1.25, lambda: webbrowser.open('http://127.0.0.1:5000') ).start()
  socketio.run(app, port=5000, debug=False)