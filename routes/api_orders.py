from flask import Blueprint, jsonify, request

from db import db
from models import Customer, Product, Order, ProductOrder

# Creates a Blueprint object (similar to Flask). Make sure you give it a name!
api_orders_bp = Blueprint("api_orders", __name__)


@api_orders_bp.route("<int:order_id>")
def order_detail_json(order_id):
    order = Order.query.get_or_404(order_id)
    return jsonify(order.to_json())


@api_orders_bp.route("/")
def orders_json():
    statement = db.select(Order).order_by(Order.id)
    results = db.session.execute(statement)
    orders = []
    for order in results.scalars():
        order_json = order.to_json()
        orders.append(order_json)

    return jsonify(orders)


@api_orders_bp.route("<int:order_id>", methods=["PUT"])
def order_put(order_id):
    order = Order.query.get(order_id)

    # Check if order exists
    if order is None:
        return "Order not found", 404

    # Check if "process" key is in JSON payload
    if "process" not in request.json or type(request.json["process"]) is not bool:
        return "Invalid or missing 'process' key in JSON payload", 400

    if request.json["process"]:
        strategy = request.json.get("strategy", "adjust")
        if strategy not in ["adjust", "reject", "ignore"]:
            return "Invalid 'strategy' key in JSON payload", 400

        # Success is a boolean, message is a string
        success, message = order.process(strategy)
        if success:
            db.session.commit()
            return "Order processed successfully", 200
        else:
            return message, 400

    return "Order not processed", 200


@api_orders_bp.route("/", methods=["POST"])
def order_post():
    # If customer_id is not in the JSON data, return 400
    if "customer_id" not in request.json:
        return "customer_id missing", 400

    # If customer_id is given but it does not exist, return 404
    customer = Customer.query.get(request.json["customer_id"])
    if customer is None:
        return "customer not found", 404

    # This line will return an empty list if "items" is not in the JSON data
    items = request.json.get("items", [])

    # Create a new order, this will not work because we need to add the items to the order
    order = Order(customer_id=customer.id)
    total = 0.0
    for item in items:
        # Find the product with the name in the item
        product = Product.query.filter_by(name=item["name"]).first()

        # If the product does not exist, return 404
        if product is None:
            return "product not found", 404

        # If the quantity is negative, return 400
        if item["quantity"] < 0:
            return "quantity cannot be negative", 400

        # If the quantity exceeds the available quantity, return 400
        if item["quantity"] > product.available:
            return "quantity exceeds available quantity for " + item["name"], 400

        product_order = ProductOrder(product_id=product.id, quantity=item["quantity"])

        # Update total
        total += product.price * item["quantity"]
        order.items.append(product_order)

    order.total = total.__round__(2)
    db.session.add(order)
    db.session.commit()
    return jsonify({"id": order.id})
