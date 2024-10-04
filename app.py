from flask import Flask, jsonify

# Import the routes here:
from routes.db import db

## Application start and route registration:
app = Flask(__name__)
app.register_blueprint(db)