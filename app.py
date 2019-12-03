from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_heroku import Heroku

app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://hlkohelnzzqgnx:bb95af5526403a48f7eae11d835e85694f0a3f47f25a0db97d8fa13699761fe0@ec2-54-221-217-204.compute-1.amazonaws.com:5432/dfr11hcpoos43a"

heroku = Heroku(app)
db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(150), nullable=False)

    def __init__(self, name, price, description):
        self.name = name
        self.price = price
        self.description = description

@app.route('/product/create', methods=["POST"])
def input_products():
    if request.content_type == "application/json":
        post_data = request.get_json()
        name = post_data.get('name')
        price = post_data.get('price')
        description = post_data.get('description')

        product = Product(name, price, description)
        db.session.add(product)
        db.session.commit()

        return jsonify("Product Added")

    return jsonify("[ERROR] REQUEST MUST BE IN JSON")

@app.route('/product/get/all', methods=["GET"])
def get_all_products():
    if request.content_type == "application/json":
        all_products = db.session.query(Product.id, Product.name, Product.price, Product.description).all()
        return jsonify(all_products)

@app.route('/product/get/<id>', methods=["GET"])
def get_product_by_id(id):
    product = db.session.query(Product.id, Product.name, Product.price, Product.description).filter(Product.id == id).first()
    return jsonify(product)

@app.route('/product/update/<id>', methods=["PUT"])
def update_product(id):
    if request.content_type == "application/json":
        put_data = request.get_json()
        name = put_data.get('name')
        price = put_data.get('price')
        description = put_data.get('description')

        product = db.session.query(Product).filter(Product.id == id).first()

        if name != None:
            product.name = name

        if price != None:
            product.price = price

        if description != None:
            product.description = description

        db.session.commit()

        return jsonify("Product Changed")

    return jsonify("Error: Must Be JsOn")

@app.route('/product/delete/<id>', methods=["DELETE"])
def delete_product(id):
    product = db.session.query(Product).filter(Product.id == id).first()
    db.session.delete(product)
    db.session.commit()
    
    return jsonify("Product Deleted")


if __name__ == "__main__":
    app.debug = True
    app.run()