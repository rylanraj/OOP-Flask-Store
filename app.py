from pathlib import Path

from flask import Flask

from db import db
from routes.api_customers import api_customers_bp
from routes.api_html import api_html_bp
from routes.api_orders import api_orders_bp
from routes.api_products import api_products_bp

# __name__ is a special variable in Python that is used to identify the name of the module.
app = Flask(__name__)
app.instance_path = Path("data").resolve()
app.config["SQLALCHEMY_DATABASE_URI"] = f'sqlite:///{app.instance_path}/store.sqlite'
db.init_app(app)

app.register_blueprint(api_html_bp)
app.register_blueprint(api_customers_bp, url_prefix="/api/customers")
app.register_blueprint(api_products_bp, url_prefix='/api/products')
app.register_blueprint(api_orders_bp, url_prefix='/api/orders')

if __name__ == '__main__':
    app.run(debug=True, port=8888)
