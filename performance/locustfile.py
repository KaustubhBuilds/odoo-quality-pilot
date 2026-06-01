"""
Locust performance tests for Odoo ERP.

Simulates real user behavior against Odoo to measure
response times, throughput, and error rates under load.

Usage:
    locust -f performance/locustfile.py --host=http://localhost:8069

Then open http://localhost:8089 for the Locust dashboard.
"""

from locust import HttpUser, between, task


class OdooUser(HttpUser):
    """
    Simulated Odoo user.

    Each instance represents one person using the system.
    When Locust spawns 50 users, it creates 50 of these
    all hitting Odoo simultaneously.

    wait_time = between(1, 3) means each user waits 1-3 seconds
    between actions, simulating real human behavior.
    """

    wait_time = between(1, 3)

    # Odoo connection settings
    db_name = "quality_pilot_db"
    login = "admin"
    password = "admin"

    def on_start(self):
        """
        Runs once when the simulated user starts.
        Logs into Odoo and stores the session.
        Every subsequent request uses this session automatically.
        """
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
        """
        Helper to make JSON-RPC calls to Odoo.
        Same format as our OdooClient but via Locust's HTTP client
        so response times are tracked automatically.
        """
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
        """
        Most common action, loading the contacts list.
        Weight 3 = runs 3x more than weight 1 tasks.
        """
        self._jsonrpc_call(
            "res.partner",
            "search_read",
            [[[], {"fields": ["name", "email", "phone"], "limit": 20}]],
            name="Browse Contacts",
        )

    @task(2)
    def search_contacts(self):
        """
        Search for contacts by name.
        Simulates a user typing in the search bar.
        """
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
        """
        Load the sales quotations list.
        """
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
        """
        Read a specific contact's details.
        Simulates clicking on a contact to view their info.
        """
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
        """
        Create a contact then immediately delete it.
        Least frequent task (weight 1).
        Cleanup prevents database pollution during load tests.
        """
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
