from flask import Flask, flash, url_for, render_template, request, redirect, send_from_directory, session, send_file
from werkzeug.utils import secure_filename
import os

import henon_arnold.encrypt as e
import henon_arnold.decrypt as d
import henon_arnold.Key as k

dirpath = os.path.realpath("imagenes")
# Determinar path donde querer guardar las imagenes
UPLOAD_FOLDER = dirpath
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def menu():
    return render_template("menu.html")


@app.route('/Desencriptar', methods=["POST", "GET"])
def decrypt():
    if "private_key" in session and "public_key" in session:
        private = session["private_key"]
        public = session["public_key"]
        if request.method == "POST":
            if "file" not in request.files:
                flash(u"No file part", "alert")
                return redirect(request.url)
            else:
                file = request.files["file"]
                if file.filename == '':
                    flash(u'No selected file', "alert")
                    return redirect(request.url)
                if file and allowed_file(file.filename):
                    try:
                        decrypt_aux(file, private, public, "decrypt")
                    except:
                        flash(u"Claves introducidas incorrectas", "alert")
                        return redirect(request.url)
                    flash("Imagen desencriptada", "info")
                    return redirect(url_for('uploaded_file',
                                            filename=file.filename))
        return render_template("decrypt.html", private_key=private, public_key=public)

    else:
        flash(u"Inserte las claves", "alert")
        return redirect(url_for("keys"))


def decrypt_aux(f, pv, pb, opt="encrypt"):
    filename = secure_filename(f.filename)
    f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    key = k.Key(pv, pb)
    if opt == "encrypt":
        e.encrypt(os.path.join(app.config['UPLOAD_FOLDER'], filename), app.config['UPLOAD_FOLDER'], key)
    else:
        d.decrypt(os.path.join(app.config['UPLOAD_FOLDER'], filename), app.config['UPLOAD_FOLDER'], key)



@app.route('/Encriptar', methods=["POST", "GET"])
def encrypt():
    if "private_key" in session and "public_key" in session:
        private = session["private_key"]
        public = session["public_key"]
        if request.method == 'POST':
            # check if the post request has the file part
            if 'file' not in request.files:
                flash(u'No file part', "alert")
                return redirect(request.url)
            file = request.files['file']
            # if user does not select file, browser also
            # submit an empty part without filename
            if file.filename == '':
                flash(u'No selected file', "alert")
                return redirect(request.url)
            if file and allowed_file(file.filename):
                try:
                    decrypt_aux(file, private, public)
                except:
                    flash("Problema con la encriptacion", "alert")
                    return redirect(request.url)

                flash("Imagen encriptada", "info")
                return redirect(url_for('uploaded_file',
                                        filename=file.filename))
        return render_template("encrypt.html", private_key=private, public_key=public)
    else:
        return redirect(url_for("keys"))


@app.route('/Keys', methods=["POST", "GET"])
def keys():
    private, public = k.genKeyPairs()
    if request.method == "POST":
        private_key = request.form["private"]
        public_key = request.form["public"]
        if private_key and public_key:
            session["private_key"] = private_key
            session["public_key"] = public_key
            return redirect(url_for("menu"))
        else:
            flash(u"Introduzca ambas claves", "alert")
            redirect(request.url)

    return render_template("keys.html", private_key=private, public_key=public)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


@app.route('/reset')
def reset():
    session.pop("primary_key", None)
    session.pop("public_key", None)
    return redirect(url_for("menu"))


@app.route('/download')
def download_file():
    # path = "html2pdf.pdf"
    # path = "info.xlsx"
    path = "imagenes/dibujo.png"
    # path = "sample.txt"
    return send_file(path, as_attachment=True)


from werkzeug.middleware.shared_data import SharedDataMiddleware

app.add_url_rule('/uploads/<filename>', 'uploaded_file',
                 build_only=True)
app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
    '/uploads': app.config['UPLOAD_FOLDER']
})

if __name__ == '__main__':
    app.run(debug=True)
