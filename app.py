import xml.etree.ElementTree as ET
from classes.CircularList import CircularLinkedList
from modules.ProcessFile import ProcessFile
from flask import Flask, render_template, url_for, request, redirect, flash

app = Flask(__name__)

# settings
app.secret_key = "mysecretkey"

CircularLinkedList = CircularLinkedList()
Machine_Selected = None
Product_Selected = None


# routes
@app.route("/")
def index():
    global CircularLinkedList
    data = CircularLinkedList
    return render_template(
        "base.html",
        data=data,
        Machine_Selected=Machine_Selected,
        Product_Selected=Product_Selected,
    )


@app.route("/new_data", methods=["POST"])
def new_data():
    global CircularLinkedList
    data = CircularLinkedList

    ProcessFile(request.files["file"], CircularLinkedList)

    return redirect(url_for("index", data=data))


@app.route("/update", methods=["POST"])
def update_Machine_Select():
    global CircularLinkedList
    Machine_Name = request.form["machine"]
    for Machine in CircularLinkedList:
        if Machine.nombre == Machine_Name:
            global Machine_Selected
            Machine_Selected = Machine
            break
    return redirect(url_for("index", Machine_Selected=Machine_Selected))


if __name__ == "__main__":
    app.run(debug=True)
