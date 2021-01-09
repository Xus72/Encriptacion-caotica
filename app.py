from flask import Flask, flash, url_for, render_template, request, redirect, send_from_directory, session
from werkzeug.utils import secure_filename
import os

import henon_arnold.encrypt as e
import henon_arnold.encrypt as d
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
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        option = request.form['opcion']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            if option == "Encriptar":
                public_key = 604905670620403574245710191030
                private_key = 747588193471049732859143835301
                key = k.Key(private_key, public_key)
                e.encrypt(os.path.join(app.config['UPLOAD_FOLDER'], filename), app.config['UPLOAD_FOLDER'], key)

                return redirect(url_for('uploaded_file',
                                        filename=filename))
    # return '''
    # <!doctype html>
    # <title>Upload new File</title>
    # <h1>Upload new File</h1>
    # <form method=post enctype=multipart/form-data>
    #   <input type=file name=file>
    #   <input type=submit value=Upload>
    # </form>
    # '''

    return render_template("index.html")


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


from werkzeug.middleware.shared_data import SharedDataMiddleware

app.add_url_rule('/uploads/<filename>', 'uploaded_file',
                 build_only=True)
app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
    '/uploads': app.config['UPLOAD_FOLDER']
})

if __name__ == '__main__':
    app.run(debug=True)
