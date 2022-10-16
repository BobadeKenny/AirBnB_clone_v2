#!/usr/bin/python3
"""starts a Flask web application:"""
from flask import Flask, render_template
from models import storage
from models.state import State
from models.amenity import Amenity

app = Flask(__name__)


@app.route("/hbnb_filters", strict_slashes=False)
def hbnb_filters():
    states = storage.all(State)
    amenities = storage.all(Amenity)
    return render_template('10-hbnb_filters.html', states=states, amenities=amenities)


@app.teardown_appcontext
def teardown(arg=None):
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
