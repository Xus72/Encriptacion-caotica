from flask import Flask, flash, url_for, render_template, request, redirect, send_from_directory, session, send_file
from werkzeug.utils import secure_filename
import os

import henon_arnold.encrypt as e
import henon_arnold.decrypt as d
import henon_arnold.Key as k

UPLOAD_FOLDER = r"D:\Fork\Encriptacion-caotica\imagenes"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    [private, public] = k.genKeyPairs()

    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        option = request.form['opcion']
        private_key = request.form['private']
        public_key = request.form['public']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            if option == "Encriptar":
                # public_key = 604905670620403574245710191030
                # private_key = 747588193471049732859143835301
                key = k.Key(private_key, public_key)
                e.encrypt(os.path.join(app.config['UPLOAD_FOLDER'], filename), app.config['UPLOAD_FOLDER'], key)
                return redirect(url_for('uploaded_file',
                                        filename=filename))

            if option == "Desencriptar":
                # public_key = 604905670620403574245710191030
                # private_key = 747588193471049732859143835301
                key = k.Key(private_key, public_key)
                d.decrypt(os.path.join(app.config['UPLOAD_FOLDER'], filename), app.config['UPLOAD_FOLDER'], key)
                return redirect(url_for('uploaded_file',
                                        filename=filename))

    return render_template("index.html", private_key=private, public_key=public)


@app.route('/menu')
def menu():
    return render_template("menu.html")


@app.route('/Desencriptar', methods=["POST", "GET"])
def decrypt():
    if "private_key" in session and "public_key" in session:
        private = session["private_key"]
        public = session["public_key"]
        if request.method == "POST":
            if "file" not in request.files:
                flash("No file part")
                return redirect(request.url)
            else:
                file = request.files["file"]
                if file.filename == '':
                    flash('No selected file')
                    return redirect(request.url)
                if file and allowed_file(file.filename):
                    decrypt_aux(file, private, public, "decrypt")
        return render_template("decrypt.html", private_key=private, public_key=public)

    else:
        flash("Inserte las claves")
        return redirect(url_for("keys"))


def decrypt_aux(f, pv, pb, opt="encrypt"):
    filename = secure_filename(f.filename)
    f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    key = k.Key(pv, pb)
    if opt == "encrypt":
        e.encrypt(os.path.join(app.config['UPLOAD_FOLDER'], filename), app.config['UPLOAD_FOLDER'], key)
        return redirect(url_for('uploaded_file',
                                filename=filename))
    else:
        d.decrypt(os.path.join(app.config['UPLOAD_FOLDER'], filename), app.config['UPLOAD_FOLDER'], key)
        return redirect(url_for('uploaded_file',
                                filename=filename))


@app.route('/Encriptar', methods=["POST", "GET"])
def encrypt():
    if "private_key" in session and "public_key" in session:
        private = session["private_key"]
        public = session["public_key"]
        if request.method == 'POST':
            # check if the post request has the file part
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            # if user does not select file, browser also
            # submit an empty part without filename
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                decrypt_aux(file, private, public)
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
            return redirect(url_for("encrypt"))
        else:
            flash("Introduzca ambas claves")
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
