"""
Locust load tests for Odoo ERP.

Usage:
    locust -f performance/locustfile.py --host=http://localhost:8069
    Open http://localhost:8089 for the dashboard.
"""

from locust import HttpUser, between, task


class OdooUser(HttpUser):
    """Simulated Odoo user with weighted task distribution."""

    wait_time = between(1, 3)

    # Odoo connection settings
    db_name = "quality_pilot_db"
    login = "admin"
    password = "admin"

    def on_start(self):
        """Authenticate with Odoo on user spawn."""

        response = self.client.post(
            "/web/session/authenticate",
            json={
                "jsonrpc": "2.0",
                "params": {
                    "db": self.db_name,
                    "login": self.login,
                    "password": self.password,
                },
            },
            name="Login",
        )

        result = response.json()
        if result.get("error"):
            raise Exception("Login failed during load test")

    def _jsonrpc_call(self, model, method, args, name):
        """Send a JSON-RPC call via Locust's tracked HTTP client."""

        response = self.client.post(
            "/jsonrpc",
            json={
                "jsonrpc": "2.0",
                "method": "call",
                "params": {
                    "service": "object",
                    "method": "execute_kw",
                    "args": [
                        self.db_name,
                        2,  # uid for admin
                        self.password,
                        model,
                        method,
                        args,
                    ],
                },
            },
            name=name,
        )
        return response

    # ----- TASKS (weighted by frequency) -----

    @task(3)
    def browse_contacts(self):
        """Load contacts list, most frequent action."""

        self._jsonrpc_call(
            "res.partner",
            "search_read",
            [[[], {"fields": ["name", "email", "phone"], "limit": 20}]],
            name="Browse Contacts",
        )

    @task(2)
    def search_contacts(self):
        """Search contacts by name."""

        self._jsonrpc_call(
            "res.partner",
            "search_read",
            [
                [[("name", "ilike", "admin")]],
                {"fields": ["name", "email"], "limit": 10},
            ],
            name="Search Contacts",
        )

    @task(2)
    def browse_sales(self):
        """Load sales quotations list."""

        self._jsonrpc_call(
            "sale.order",
            "search_read",
            [
                [
                    [],
                    {
                        "fields": ["name", "partner_id", "state", "amount_total"],
                        "limit": 20,
                    },
                ]
            ],
            name="Browse Sales",
        )

    @task(2)
    def read_contact_api(self):
        """Find and read a single contact's details."""

        # First find a contact
        search_response = self._jsonrpc_call(
            "res.partner",
            "search",
            [[[("is_company", "=", False)]], {"limit": 1}],
            name="Find Contact",
        )

        result = search_response.json().get("result", [])
        if result:
            self._jsonrpc_call(
                "res.partner",
                "read",
                [
                    [result[0]],
                    {"fields": ["name", "email", "phone", "mobile", "street", "city"]},
                ],
                name="Read Contact Detail",
            )

    @task(1)
    def create_and_delete_contact(self):
        """Create then delete a contact, least frequent action."""
        import random
        import string

        random_name = "LoadTest_" + "".join(random.choices(string.ascii_letters, k=8))

        # Create
        create_response = self._jsonrpc_call(
            "res.partner",
            "create",
            [[{"name": random_name}]],
            name="Create Contact",
        )

        # Cleanup — delete what we just created
        result = create_response.json().get("result")
        if result:
            self._jsonrpc_call(
                "res.partner",
                "unlink",
                [[[result]]],
                name="Delete Contact (cleanup)",
            )
