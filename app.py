import xml.etree.ElementTree as ET
from classes.CircularList import CircularLinkedList
from classes.LinkedLists import ProductLinkedList
from modules.ProcessFile import ProcessFile, simulate_assembly
from modules.ExportFile import generate_output_xml
from modules.GenerateGraphTDA import generate_tda_report

from flask import Flask, render_template, url_for, request, redirect

app = Flask(__name__)

# settings
app.secret_key = "mysecretkey"

CircularLinkedList = CircularLinkedList()
ReportLinkedList = ProductLinkedList()
Machine_Selected = None
Product_Selected = None

actionsAssembly = None
timeProduct = None


# routes frontend
@app.route("/")
def index():
    global CircularLinkedList
    data = CircularLinkedList
    return render_template(
        "Data_Gestion.html",
        data=data,
        Machine_Selected=Machine_Selected,
        Product_Selected=Product_Selected,
        actionsAssembly=actionsAssembly,
        ReportLinkedList=ReportLinkedList,
    )


@app.route("/Simulation")
def Simulation():
    return render_template(
        "Simulation.html",
        Machine_Selected=Machine_Selected,
        Product_Selected=Product_Selected,
        actionsAssembly=actionsAssembly,
        ReportLinkedList=ReportLinkedList,
    )


@app.route("/Reports")
def Reports():
    return render_template("Reports.html", ReportLinkedList=ReportLinkedList)


# routes backend
@app.route("/new_data", methods=["POST"])
def new_data():
    global CircularLinkedList
    data = CircularLinkedList

    ProcessFile(request.files["file"], CircularLinkedList)

    return redirect(url_for("index", data=data))


@app.route("/updateMachine", methods=["POST"])
def update_Machine_Select():
    global CircularLinkedList
    global Machine_Selected
    Machine_Name = request.form["machine"]
    for Machine in CircularLinkedList:
        if Machine.nombre == Machine_Name:
            global Machine_Selected
            Machine_Selected = Machine
            break
    generate_output_xml(CircularLinkedList)

    return redirect(url_for("index", Machine_Selected=Machine_Selected))


@app.route("/updateProduct", methods=["POST"])
def update_Product_Select():
    global Machine_Selected
    global Product_Selected
    global actionsAssembly
    global ReportLinkedList
    global Machine_Selected

    Product_Name = request.form["product"]
    for Product in Machine_Selected.productos:
        if Product.nombre == Product_Name:
            global Product_Selected
            Product_Selected = Product
            break

    actionsAssembly = simulate_assembly(Machine_Selected, Product_Selected)

    for action in actionsAssembly:
        ReportLinkedList.append(
            action.name,
            action.total_time,
            action.secondsActions,
            action.lineas_produccion,
        )
        for time in action.secondsActions:
            print(time.second)
            for actionTime in time.actions:
                print(actionTime)

    generate_tda_report(Machine_Selected, Product_Selected.nombre, 10)
    return redirect(
        url_for(
            "index",
            Product_Selected=Product_Selected,
            actionsAssembly=actionsAssembly,
            ReportLinkedList=ReportLinkedList,
        )
    )


@app.route("/generate", methods=["POST"])
def generate():
    global CircularLinkedList
    global Machine_Selected
    generate_output_xml(CircularLinkedList)

    return redirect(url_for("index", Machine_Selected=Machine_Selected))


if __name__ == "__main__":
    app.run(debug=True)
