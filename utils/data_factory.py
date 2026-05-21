from faker import Faker

# Create one Faker instance at module level
# WHY: Creating Faker() once and reusing it is more efficient
# than creating a new instance in every function call
fake = Faker()


def generate_contact() -> dict:
    """
    Generate realistic random contact data for Odoo Contacts module.
    Returns a dictionary with all fields needed to create a contact.
    Every call returns completely different data — no conflicts between tests.

    Returns:
        dict: contact data with name, email, phone, mobile, company
    """
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
    """
    Generate realistic random lead data for CRM tests.
    Each test run gets unique customer name, opportunity title,
    and expected revenue.

    Returns:
        dict: lead data with customer, opportunity, revenue, lost_reason
    """
    customer_id = fake.random_int(min=100, max=9999)
    opportunity_id = fake.random_int(min=1, max=999)
    return {
        "customer": (f"{fake.first_name()} {fake.last_name()} {customer_id}"),
        "opportunity": (f"{fake.bs().title()} Lead {opportunity_id}"),
        "expected_revenue": str(fake.random_int(min=1000, max=50000)),
        "lost_reason": "Not enough stock",
    }


def generate_product() -> dict:
    """
    Generate realistic random product data for Odoo Inventory module.

    Returns:
        dict: product data with name, price, internal reference
    """
    return {
        "name": f"{fake.word().title()} {fake.word().title()} Product",
        "price": round(fake.random_number(digits=3) + 0.99, 2),
        "internal_ref": fake.bothify("PROD-????-###").upper(),
    }


def generate_sales_order() -> dict:
    """
    Generate realistic random sales order data.

    Returns:
        dict: sales order data
    """
    return {
        "customer": fake.company(),
        "reference": fake.bothify("SO-????-###").upper(),
    }
