import os
from flask import Flask, render_template, jsonify, send_from_directory, current_app
from gevent import monkey; monkey.patch_all()
from gevent.pywsgi import WSGIServer

from database import load_pg_from_db

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.route("/")
def hello_pm1():
  pgn = load_pg_from_db()
  return render_template('home.html',
                        pgn=pgn)



@app.route('/tema/<int:tema_id>')
def show_tema(tema_id):
    # Supongamos que TEMAS es tu estructura de datos (lista o dict)
    tema = pgn[tema_id]
    return render_template('classpage.html', i=tema)
  

@app.route("/api/temas")
def list_temas():
  return jsonify(pgn)



@app.route('/download/<path:filename>')
def download_file(filename):
    filename = secure_filename(filename)
    static_folder = current_app.static_folder  # Usually 'static'
    return send_from_directory(static_folder, filename, as_attachment=True)
  

if __name__ == '__main__':
    http_server = WSGIServer(('0.0.0.0', 8080), app)
    http_server.serve_forever()