# Import Modules
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_heroku import Heroku

app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"]

heroku = Heroku(app)
db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    price = db.Column(db.Decimal, nullable=False)
    description = db.Column(db.String(150), nullable=False)

    def __init__(self, name, price, description):
        self.name = name
        self.price = price
        self.description = description

@app.route('product/create', methods=["POST"])
def input_products(name, price, description):
    if request.content_type == "application/json":
        post_data = request.get_json()
        name = post_data.get('name')
        price = post_data.get('price')
        description = post_data.get('description')

        return jsonify("Product Added")

    return jsonify("[ERROR] REQUEST MUST BE IN JSON")

# @app.route('product/get/all', methods=["GET"])

# @app.route('product/get/<id>')
# Builld Classes

# Build Model

# Build Endpoints

# Dunder Name Dunder Main