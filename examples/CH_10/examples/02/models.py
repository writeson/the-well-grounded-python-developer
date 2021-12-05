import os
import csv
from pathlib import Path
from contextlib import contextmanager
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


# erase and create the database
db_filepath = Path(__file__).parent / "transaction.sqlite"
if db_filepath.exists():
    os.remove(db_filepath)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///transaction.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app, session_options={"autoflush": False})


@contextmanager
def session_manager():
    try:
        yield db.session
    except Exception:
        db.session.rollback()
        raise
    finally:
        db.session.close()


class Customer(db.Model):
    __tablename__ = "customer"
    customer_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    orders = db.relationship("Order", backref=db.backref("customer"))


class Address(db.Model):
    __tablename__ = "address"
    address_id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String)
    zipcode = db.Column(db.String)
    orders = db.relationship("Order", backref=db.backref("address"))


class Order(db.Model):
    __tablename__ = "order"
    order_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.customer_id"))
    address_id = db.Column(db.Integer, db.ForeignKey("address.address_id"))


class Product(db.Model):
    ___tablename__ = "product"
    product_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)


class Item(db.Model):
    __tablename__ = "item"
    order_id = db.Column(db.Integer, db.ForeignKey("order.order_id"), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("product.product_id"), primary_key=True)
    qty = db.Column(db.Integer)
    order = db.relationship("Order", backref=db.backref("items"))
    product = db.relationship("Product")


class CsvData:
    """This class reads, contains and provides the data for
    a CSV file where the first field is the unique id
    """

    def __init__(self, filename):
        self.data = {}
        filepath = Path(__file__).parent / filename
        with open(filepath, "r") as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                self.data[row[next(iter(row))]] = row


# create the database
db.create_all()


def load_database():
    customers = CsvData("customer.csv")
    addresses = CsvData("address.csv")
    orders = CsvData("order.csv")
    products = CsvData("product.csv")
    items = CsvData("item.csv")

    with session_manager() as session:
        # create the customers
        for customer in customers.data.values():
            session.add(Customer(
                name=customer.get("name")
            ))

        # create addresses
        for address in addresses.data.values():
            session.add(Address(
                street=address.get("street"),
                zipcode=address.get("zipcode")
            ))
        # create products
        for product in products.data.values():
            session.add(Product(
                name=product.get("name")
            ))
        # commit these items
        session.commit()

        # build a map of orders
        orders_map = {str(index): Order() for index, order in enumerate(orders.data.values(), start=1)}

        # build the orders and items
        for item in items.data.values():
            # get the order_id and order associated with this item
            order_id = item.get("order_id")
            order = orders_map.get(order_id)

            # get the customer, address and product associated with the item
            customer_id = orders.data.get(order_id).get("customer_id")
            customer = session.query(Customer).filter(Customer.customer_id == customer_id).one_or_none()
            address_id = orders.data.get(order_id).get("address_id")
            address = session.query(Address).filter(Address.address_id == address_id).one_or_none()

            if order.customer is None:
                order.customer = customer
            if order.address is None:
                order.address = address

            # create an item with it's many-to-many associations
            product_id = item.get("product_id")
            product = session.query(Product).filter(Product.product_id == product_id).one_or_none()
            new_item = Item(
                qty=item.get("qty")
            )
            new_item.product = product
            order.items.append(new_item)

        # add the populated orders to the session and database
        for order in orders_map.values():
            session.add(order)
        session.commit()
