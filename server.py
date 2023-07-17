import threading, webbrowser
from flask import Flask, request, current_app, make_response, render_template
from flask_cors import CORS
from flask_socketio import SocketIO
from printerInterface import wait_for_print_job
from querydb import querydb, get_countries, get_provinces, get_families

app = Flask(__name__, static_url_path='', static_folder='dist')
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