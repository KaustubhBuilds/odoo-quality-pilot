from faker import Faker

fake = Faker()


def generate_contact() -> dict:
    """Generate random contact data for Odoo Contacts tests."""

    first_name = fake.first_name()
    last_name = fake.last_name()
    return {
        "name": f"{first_name} {last_name}",
        "email": f"{first_name.lower()}.{last_name.lower()}"
        f"{fake.random_int(min=1, max=999)}@testmail.com",
        "phone": fake.numerify("+49 ### #######"),
        "mobile": fake.numerify("+49 1## #######"),
        "company": fake.company(),
        "street": fake.street_address(),
        "city": fake.city(),
    }


def generate_lead() -> dict:
    """Generate random lead data for CRM tests."""

    customer_id = fake.random_int(min=100, max=9999)
    opportunity_id = fake.random_int(min=1, max=999)
    return {
        "customer": (f"{fake.first_name()} {fake.last_name()} {customer_id}"),
        "opportunity": (f"{fake.bs().title()} Lead {opportunity_id}"),
        "expected_revenue": str(fake.random_int(min=1000, max=50000)),
        "lost_reason": "Not enough stock",
    }


def generate_product() -> dict:
    """Generate random product data for Inventory tests."""

    return {
        "name": f"{fake.word().title()} {fake.word().title()} Product",
        "price": round(fake.random_number(digits=3) + 0.99, 2),
        "internal_ref": fake.bothify("PROD-????-###").upper(),
    }


def generate_sales_order() -> dict:
    """Generate random sales order data."""

    return {
        "customer": fake.company(),
        "reference": fake.bothify("SO-????-###").upper(),
    }
