from flask import Blueprint, jsonify, request
from db import db
from models import Customer

# Creates a Blueprint object (similar to Flask). Make sure you give it a name!
api_customers_bp = Blueprint("api_customers", __name__)


@api_customers_bp.route("/", methods=["GET"])
def api_customer_list():
    stmt = db.select(Customer).order_by(Customer.name)
    results = db.session.execute(stmt).scalars()
    return jsonify([cust.to_json() for cust in results])


@api_customers_bp.route("/<int:customer_id>", methods=["GET"])
def customer_detail_json(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    return jsonify(customer.to_json())


@api_customers_bp.route("/", methods=["POST"])
def customer_post():
    print(request.json)

    if "name" not in request.json or "phone" not in request.json:
        return "missing data", 400

    if request.json["name"] == "" or request.json["phone"] == "":
        return "missing data", 400

    # We will create a new customer here and return the new customer's id
    customer = Customer(name=request.json["name"], phone=request.json["phone"])
    db.session.add(customer)
    db.session.commit()
    return jsonify({"id": customer.id})


@api_customers_bp.route("<int:customer_id>", methods=["DELETE"])
def customer_delete(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    db.session.delete(customer)
    db.session.commit()
    return "deleted"


@api_customers_bp.route("<int:customer_id>", methods=["PUT"])
def customer_put(customer_id):
    print(request.json)
    # Receives JSON data for balance and updates the balance for customer 1234
    customer = Customer.query.get(customer_id)
    if request.json["balance"] == "":
        return "missing data", 400

    customer.balance = request.json["balance"]
    db.session.commit()
    return "putted"
