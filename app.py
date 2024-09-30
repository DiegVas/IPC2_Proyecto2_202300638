

import xml.etree.ElementTree as ET
from classes.CircularList import CircularLinkedList
from modules.ProcessFile import ProcessFile
from flask import Flask, render_template, url_for, request, redirect, flash

app = Flask(__name__)

# settings
app.secret_key = "mysecretkey"

CircularLinkedList = CircularLinkedList()

# routes
@app.route('/')
def index():
    return render_template('base.html')

@app.route('/new_data', methods=['POST'])
def new_data():
    global CircularLinkedList
    
    ProcessFile(request.files['file'], CircularLinkedList)
    
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
