#!/usr/bin/python3
"""starts a Flask web application:"""
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.route("/states", strict_slashes=False)
@app.route("/states/<id>", strict_slashes=False)
def states_list(id=None):
    return render_template('9-states.html', states=storage.all(State))


@app.teardown_appcontext
def teardown(arg=None):
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
