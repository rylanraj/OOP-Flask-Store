from flask import Blueprint, render_template, redirect, url_for

from db import db
from models import Customer, Product, Order

# Creates a Blueprint object (similar to Flask). Make sure you give it a name!
api_html_bp = Blueprint("api_html", __name__)


@api_html_bp.route('/home')
def home_message():
    return render_template('home.html', name='user')


@api_html_bp.route('/')
def home():
    return render_template('home.html')


@api_html_bp.route('/customers')
def customer():
    customers = Customer.query.all()
    return render_template('customers.html', customers=customers)


@api_html_bp.route('/products')
def product():
    products = Product.query.all()
    return render_template('products.html', products=products)


@api_html_bp.route("/orders")
def orders():
    orders = Order.query.all()
    return render_template('orders.html', orders=orders)


@api_html_bp.route("/customer/<int:customer_id>")
def customer_detail(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    return render_template('customer_detail.html', customer=customer)


@api_html_bp.route("/order/<int:order_id>")
def order_detail(order_id):
    order = Order.query.get_or_404(order_id)
    return render_template('order_detail.html', order=order)


# Delete orders using post method, also uses url_for and redirect
@api_html_bp.route("/orders/<int:order_id>/delete", methods=["POST"])
def order_delete(order_id):
    order = db.get_or_404(Order, order_id)
    if order.processed:
        return "Cannot delete processed order", 400

    db.session.delete(order)
    db.session.commit()
    return redirect(url_for('api_html.orders'))


@api_html_bp.route("/orders/<int:order_id>/process", methods=["POST"])
def order_process(order_id):
    order = db.get_or_404(Order, order_id)
    if order.processed:
        return "Order already processed", 400

    success, message = order.process()
    if success:
        db.session.commit()
        return redirect(url_for('api_html.orders'))
    else:
        return message, 400
