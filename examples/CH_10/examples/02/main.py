import os
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
from models import load_database, Order, session_manager


def create_invoice(order):
    """Create the PDF invoice for the order

    Args:
        info (dict): The info information to generate the invoice with
    """
    invoice_filename = f"invoice_{order.order_id}.pdf"

    # delete existing order invoice file if exists
    if os.path.exists(invoice_filename):
        os.remove(invoice_filename)

    # set up Jinja2 to generate the HTML and then the PDF file
    path = Path(__file__).parent
    env = Environment(loader=FileSystemLoader(Path(path)))
    template = env.get_template("invoice_template.jinja")
    html_out = template.render(order=order)
    HTML(string=html_out).write_pdf(
        invoice_filename,
        stylesheets=[
            "page.css",
            "bootstrap.css",
        ]
    )


# load the database
load_database()

# generate an invoice file for all the orders
with session_manager() as session:
    for order in session.query(Order).all():
        create_invoice(order)
