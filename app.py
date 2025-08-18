import os
from flask import Flask, render_template, jsonify, send_from_directory, current_app
from gevent import monkey; monkey.patch_all()
from gevent.pywsgi import WSGIServer
from database import load_pg_from_db, load_pgn_from_db
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.route("/")
def hello_pm1():
  pgn = load_pg_from_db()
  return render_template('home.html',
                        pgn=pgn)



@app.route('/pgn/<int:pgn_id>') 
def show_pgn(pgn_id):
    # Supongamos que TEMAS es tu estructura de datos (lista o dict)
    pgn = load_pg_from_db()
    item = next((item for item in pgn if item['id'] == pgn_id), None)
    if item is None:
        return "Not Found", 404
    return render_template('classpage.html', i=item)

  
@app.route("/pgn/<id>")
def show_a_pgn(id):
    pgn = load_pgn_from_db(id)
    return jsonify(pgn)



@app.route('/download/<path:filename>')
def download_file(filename):
    filename = secure_filename(filename)
    static_folder = current_app.static_folder  # Usually 'static'
    return send_from_directory(static_folder, filename, as_attachment=True)
  

if __name__ == '__main__':
    http_server = WSGIServer(('0.0.0.0', 8080), app)
    http_server.serve_forever()