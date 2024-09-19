# app.py
from flask import Flask, render_template, url_for

app = Flask(__name__)


@app.route("/file")
def file():
    return render_template("/layouts/File.html")


@app.route("/")
def home():
    return render_template("/layouts/Process.html")


@app.route("/help")
def help():
    return render_template("/layouts/Report.html")


if __name__ == "__main__":
    app.run(debug=True)
