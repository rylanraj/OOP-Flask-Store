from flask import Blueprint, jsonify, request, render_template
from db import db
from models import Customer, Product, Order

# Creates a Blueprint object (similar to Flask). Make sure you give it a name!
api_products_bp = Blueprint("api_products", __name__)


@api_products_bp.route("/")
def products_json():
    statement = db.select(Product).order_by(Product.name)
    results = db.session.execute(statement)
    products = []
    for product in results.scalars():
        product_json = product.to_json()
        products.append(product_json)

    return jsonify(products)


@api_products_bp.route("<int:product_id>", methods=["DELETE"])
def product_delete(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return "deleted"


@api_products_bp.route("/", methods=["POST"])
def product_post():
    print(request.json)

    if request.json["price"] < 0:
        return "price cannot be negative", 400

    if "name" not in request.json or "price" not in request.json:
        return "missing data", 400

    if request.json["name"] == "" or request.json["price"] == "":
        return "missing data", 400

    product = Product(name=request.json["name"], price=request.json["price"])
    db.session.add(product)
    db.session.commit()
    return jsonify({"id": product.id})


@api_products_bp.route("<int:product_id>", methods=["PUT"])
def product_put(product_id):
    print(request.json)
    product = Product.query.get(product_id)

    # Give options to update available, price, and name
    if "available" in request.json:
        product.available = request.json["available"]

    if "price" in request.json:
        if request.json["price"] < 0:
            return "price cannot be negative", 400

        product.price = request.json["price"]

    if "name" in request.json:
        product.name = request.json["name"]

    db.session.commit()
    return "putted"
