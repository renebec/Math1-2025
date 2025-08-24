import os
from flask import Flask, render_template, jsonify, redirect, request, url_for, flash, send_from_directory, current_app
from gevent import monkey; monkey.patch_all()
from gevent.pywsgi import WSGIServer
from database import load_pg_from_db, load_pgn_from_db
from werkzeug.utils import secure_filename

import cloudinary
import cloudinary.uploader

from database import load_pgn_from_db, insert_actividad



@app.route("/actividad/<int:id>", methods=["GET", "POST"])
def show_actividad(id):
    actividad = load_pgn_from_db(id)

    if not actividad:
        return render_template("error.html", message="actividad no encontrada."), 404

    if request.method == "POST":
        # Obtener datos del formulario
        apellido_paterno = request.form['apellido_paterno']
        apellido_materno = request.form['apellido_materno']
        nombres = request.form['nombres']
        pdf_file = request.files['pdf_file']

        # Validar PDF
        if not pdf_file or not pdf_file.filename.endswith('.pdf'):
            flash("Debes subir un archivo PDF válido.", "danger")
            return redirect(request.url)

        # Subir a Cloudinary
        result = cloudinary.uploader.upload(
            pdf_file,
            resource_type='raw',
            folder='actividades_pdf'
        )

        pdf_url = result['secure_url']

        # Guardar en base de datos
        insert_actividad(id, actividad_num, apellido_paterno, apellido_materno, nombres, carrera, semestre, grupo, pdf_url)
        flash("Actividad enviada correctamente.", "success")
        return redirect(url_for("show_actividad", id=id))

    return render_template("classpage.html", actividad=actividad)



app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.route("/")
def hello_pm1():
  pg = load_pg_from_db()
  return render_template('home.html',
                        pg=pg)



@app.route('/pg/<int:pg_id>') 
def show_pg(pg_id):
    # Supongamos que TEMAS es tu estructura de datos (lista o dict)
    pg = load_pg_from_db()
    item = next((item for item in pg if item['id'] == pg_id), None)
    if item is None:
        return "Not Found", 404
    return render_template('classpage.html', i=item)

  
@app.route("/pgn/<int:id>")
def show_pgn(id):
    pgn = load_pgn_from_db(id)
    if pgn:
        return jsonify(pgn)
    else:
        return jsonify({'error': 'Not found'}), 404


@app.route("/test-insert")
def test_insert():
    insert_solicitud(1, "actividad 1", "García", "López", "Juan Carlos", "TA", "5", "A", "https://example.com/test.pdf")
    return "Insert test completed"




if __name__ == '__main__':
    http_server = WSGIServer(('0.0.0.0', 8080), app)
    http_server.serve_forever()