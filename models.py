from datetime import datetime

from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import mapped_column, relationship

from db import db


class Order(db.Model):
    # db.Column is a class that represents a column in a database table.
    id = db.Column(db.Integer, primary_key=True)
    total = mapped_column(Float(2), nullable=False, default=0)
    # Get the customer_id from the Customer table (the primary key of the Customer table)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    # Now we can access the customer object from the order object
    customer = relationship("Customer", back_populates="orders")
    items = relationship("ProductOrder", cascade="all, delete-orphan", back_populates="order")
    # Whenever an order is created, the created column will be set to the current time
    created = mapped_column(db.DateTime, nullable=False, server_default=db.func.now())
    # Processed represents when the order is processed by the store, by default it is null
    processed = mapped_column(db.DateTime, nullable=True, default=None)

    def process(self, strategy='adjust'):
        if self.processed is not None:
            return False, "Order has already been processed"

        if self.customer.balance <= 0:
            return False, "Customer balance is insufficient"

        total_price = 0.00
        for item in self.items:
            if item.quantity > item.product.available:
                if strategy == 'adjust':
                    item.quantity = item.product.available
                elif strategy == 'reject':
                    return False, f"Insufficient quantity for product {item.product.name}"
                elif strategy == 'ignore':
                    item.quantity = 0

            item.product.available -= item.quantity
            total_price += item.quantity * item.product.price

        if self.customer.balance < total_price:
            # Add the quantity back to the available quantity
            for item in self.items:
                item.product.available += item.quantity

            return False, "Customer balance is insufficient after order calculation"

        self.customer.balance -= total_price

        self.total = round(total_price, 2)
        self.processed = datetime.now()

        return True, "Order processed successfully"

    def compute_total(self):
        total = 0.0
        for item in self.items:
            total += item.product.price * item.quantity
        return round(total, 2)  # Round the total to 2 decimal places

    def update_total(self):
        self.total = self.compute_total()

    def to_json(self):
        return {
            "id": self.id,
            "total": self.total,
            "customer_id": self.customer_id,
            "items": [{"product_id": item.product_id, "quantity": item.quantity} for item in self.items],
            "created": self.created.strftime("%Y-%m-%d %H:%M:%S"),
            "processed": self.processed.strftime("%Y-%m-%d %H:%M:%S") if self.processed is not None else None
        }


class ProductOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    product = relationship("Product")
    order = relationship("Order", back_populates="items")
    quantity = db.Column(db.Integer, nullable=False, default=0)


class Customer(db.Model):
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(200), nullable=False, unique=True)
    phone = mapped_column(String(20), nullable=False)
    balance = mapped_column(Float(2), nullable=False, default=0)
    orders = relationship("Order", back_populates="customer")

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone,
            "balance": float(self.balance)  # Convert to float for JSON serialization
        }


class Product(db.Model):
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(200), nullable=False, unique=True)
    price = mapped_column(Float(20), nullable=False)
    available = mapped_column(Integer, nullable=False, default=0)

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": float(self.price),  # Convert to float for JSON serialization
            "available": self.available
        }
