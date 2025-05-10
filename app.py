# app.py
from flask import Flask, render_template, request, jsonify
from model import train_eval

app = Flask(__name__)
history = [] 
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/train", methods=["POST"])
def train():
    data    = request.get_json()
    algo    = data["algo"]                 # e.g. "svm"
    hp      = data["hyperparams"]          # dict of strings
    result  = train_eval(algo, hp)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
