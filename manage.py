from db import db
from app import app
from models import Customer, Product, Order, ProductOrder
from sqlalchemy.sql import func
from pathlib import Path
import csv
import random

app.instance_path = Path("data").resolve()
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{app.instance_path}/store.db'


def csv_to_list(file):
    temp = []
    with open(file, "r") as file:
        csv_reader = csv.DictReader(file, delimiter=',')
        for row in csv_reader:
            temp.append(row)
        return temp


def create_random_orders(num_orders):
    for _ in range(num_orders):
        # Select a random customer
        customer = db.session.query(Customer).order_by(func.random()).limit(1).scalar()

        # Create a new order for the customer
        order = Order(customer=customer)
        db.session.add(order)

        # Select a random product
        product = db.session.query(Product).order_by(func.random()).limit(1).scalar()

        # Generate a random quantity between 10 and 20
        quantity = random.randint(10, 20)

        # Add the product to the order with the random quantity
        product_order = ProductOrder(order=order, product=product, quantity=quantity)
        db.session.add(product_order)

    # Commit all changes to the database
    db.session.commit()

    # After adding all products to orders, update the total for each order
    orders = Order.query.all()
    for order in orders:
        order.update_total()
    db.session.commit()


if __name__ == "__main__":
    with app.app_context():
        db.drop_all()
        db.create_all()
        # obj = Customer(name="Tim", phone=123)
        # db.session.add(obj)
        customer_list = csv_to_list("data/customers.csv")
        for row in customer_list:
            customer = Customer(name=row["name"], phone=row["phone"])
            db.session.add(customer)

        product_list = csv_to_list("data/products.csv")
        for row in product_list:
            product = Product(name=row["name"], price=row["price"])
            db.session.add(product)
        db.session.commit()
        num_orders = 10  # Specify the number of random orders to create
        create_random_orders(num_orders)
