"""
Odoo JSON-RPC API Client.

This is the 'phone' that talks to Odoo directly no browser needed.
Every method sends a JSON message to Odoo's /jsonrpc endpoint
and returns the result.

Usage:
    client = OdooClient()
    client.authenticate()
    contact_id = client.create("res.partner", {"name": "John"})
    contact = client.read("res.partner", [contact_id])
"""

import requests

from config.settings import settings


class OdooClient:
    """
    Reusable JSON-RPC client for Odoo.

    Think of this like a page object, but for the API layer.
    Page objects wrap browser actions. This wraps API calls.
    Same principle: write once, use in every test.
    """

    def __init__(self):
        # Read connection details from .env via settings
        # Same settings the UI tests use — single source of truth
        self.base_url = settings.BASE_URL
        self.database = settings.ODOO_DB
        self.username = settings.ODOO_USER
        self.password = settings.ODOO_PASSWORD

        # The JSON-RPC endpoint — all API calls go here
        self.url = f"{self.base_url}/jsonrpc"

        # User ID — set after authentication
        # None means "not logged in yet"
        self.uid = None

    def _jsonrpc(self, service: str, method: str, args: list):
        """
        Send a JSON-RPC request to Odoo and return the result.

        This is the private helper that every public method uses.
        It handles the message format so other methods don't repeat it.

        Args:
            service: 'common' for auth, 'object' for CRUD operations
            method: the Odoo method to call ('authenticate', 'execute_kw')
            args: list of arguments the method needs

        Returns:
            The result from Odoo (could be an ID, a list, a dict, etc.)

        Raises:
            Exception: if Odoo returns an error
        """
        # Build the JSON-RPC message, this format is required by Odoo
        payload = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "service": service,
                "method": method,
                "args": args,
            },
        }

        # Send the message and get the response
        response = requests.post(self.url, json=payload)
        result = response.json()

        # Check if Odoo returned an error
        if result.get("error"):
            error_msg = (
                result["error"].get("data", {}).get("message", "Unknown Odoo error")
            )
            raise Exception(f"Odoo API error: {error_msg}")

        return result.get("result")

    def authenticate(self):
        """
        Log in to Odoo and store the user ID.

        This must be called before any other method.
        Think of it as picking up the phone and saying who you are.

        Returns:
            int: the user ID (uid), Odoo's way of knowing who you are
        """
        self.uid = self._jsonrpc(
            "common",
            "authenticate",
            [self.database, self.username, self.password, {}],
        )

        if not self.uid:
            raise Exception(f"Authentication failed for {self.username}")

        return self.uid

    def create(self, model: str, values: dict) -> int:
        """
        Create a new record in Odoo.

        Args:
            model: Odoo model name (e.g. 'res.partner' for contacts)
            values: dict of field names and values

        Returns:
            int: the ID of the newly created record

        Example:
            contact_id = client.create("res.partner", {"name": "John"})
        """
        return self._jsonrpc(
            "object",
            "execute_kw",
            [
                self.database,
                self.uid,
                self.password,
                model,
                "create",
                [values],
            ],
        )

    def read(self, model: str, ids: list, fields: list = None) -> list:
        """
        Read records by their IDs.

        Args:
            model: Odoo model name
            ids: list of record IDs to read
            fields: optional list of field names to return

        Returns:
            list of dicts, one per record

        Example:
            contacts = client.read("res.partner", [42], ["name", "email"])
        """
        kwargs = {}
        if fields:
            kwargs["fields"] = fields

        return self._jsonrpc(
            "object",
            "execute_kw",
            [
                self.database,
                self.uid,
                self.password,
                model,
                "read",
                [ids],
                kwargs,
            ],
        )

    def search(self, model: str, domain: list, limit: int = None) -> list:
        """
        Search for records matching a condition.

        Args:
            model: Odoo model name
            domain: search filter as a list of tuples
                    e.g. [("name", "=", "John")]
            limit: max number of results

        Returns:
            list of matching record IDs

        Example:
            ids = client.search("res.partner", [("name", "=", "John")])
        """
        kwargs = {}
        if limit:
            kwargs["limit"] = limit

        return self._jsonrpc(
            "object",
            "execute_kw",
            [
                self.database,
                self.uid,
                self.password,
                model,
                "search",
                [domain],
                kwargs,
            ],
        )

    def write(self, model: str, ids: list, values: dict) -> bool:
        """
        Update existing records.

        Args:
            model: Odoo model name
            ids: list of record IDs to update
            values: dict of fields to change

        Returns:
            True if successful

        Example:
            client.write("res.partner", [42], {"name": "Jane"})
        """
        return self._jsonrpc(
            "object",
            "execute_kw",
            [
                self.database,
                self.uid,
                self.password,
                model,
                "write",
                [ids, values],
            ],
        )

    def unlink(self, model: str, ids: list) -> bool:
        """
        Delete records.

        Args:
            model: Odoo model name
            ids: list of record IDs to delete

        Returns:
            True if successful

        Example:
            client.unlink("res.partner", [42])
        """
        return self._jsonrpc(
            "object",
            "execute_kw",
            [
                self.database,
                self.uid,
                self.password,
                model,
                "unlink",
                [ids],
            ],
        )

    def search_read(
        self, model: str, domain: list, fields: list = None, limit: int = None
    ) -> list:
        """
        Search and read in one call, the most efficient way to find data.

        Combines search() + read() into a single API call.
        Use this when you need both the filter and the data.

        Args:
            model: Odoo model name
            domain: search filter
            fields: field names to return
            limit: max results

        Returns:
            list of dicts with the matching records and their fields

        Example:
            contacts = client.search_read(
                "res.partner",
                [("name", "like", "John")],
                fields=["name", "email"],
                limit=5
            )
        """
        kwargs = {}
        if fields:
            kwargs["fields"] = fields
        if limit:
            kwargs["limit"] = limit

        return self._jsonrpc(
            "object",
            "execute_kw",
            [
                self.database,
                self.uid,
                self.password,
                model,
                "search_read",
                [domain],
                kwargs,
            ],
        )
