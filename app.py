from flask import Flask, url_for,render_template, request

app = Flask(__name__)

@app.route('/', methods =["POST", "GET"])

def index():
    return render_template("index.html", name="Index")


if __name__ == '__main__':
    app.run(debug=True)