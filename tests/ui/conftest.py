"""UI test fixtures for state-controlled testing.

These fixtures create explicit test data via the API instead of relying on
demo data ordering. This ensures tests are reproducible on any fresh install.
"""

import uuid

import pytest

from services.odoo_client import OdooClient


@pytest.fixture(scope="function")
def customer_with_contact_info():
    """Create a customer with email/phone via API, yield it, then clean up."""
    client = OdooClient()
    client.authenticate()

    unique_name = f"TestCustomer_{uuid.uuid4().hex[:8]}"
    customer_data = {
        "name": unique_name,
        "email": f"{unique_name.lower()}@example.com",
        "phone": "+49 123 4567890",
        "is_company": False,
    }

    customer_id = client.create("res.partner", customer_data)

    yield {
        "id": customer_id,
        "name": unique_name,
        "email": customer_data["email"],
        "phone": customer_data["phone"],
    }

    try:
        client.unlink("res.partner", [customer_id])
    except Exception:
        pass


@pytest.fixture(scope="function")
def storable_product():
    """Create a storable product via API so Delivery button appears on confirm.

    Odoo 17: type='consu' with is_storable=True is the storable-product
    equivalent (replaces the old 'product' type).
    """
    client = OdooClient()
    client.authenticate()

    unique_name = f"TestProduct_{uuid.uuid4().hex[:8]}"
    product_id = client.create(
        "product.product",
        {
            "name": unique_name,
            "type": "consu",
            "is_storable": True,
            "list_price": 100.0,
            "sale_ok": True,
        },
    )

    yield {"id": product_id, "name": unique_name}

    try:
        client.unlink("product.product", [product_id])
    except Exception:
        pass
