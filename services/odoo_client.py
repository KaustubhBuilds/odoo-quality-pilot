"""Odoo JSON-RPC API client for direct backend operations."""

import requests

from config.settings import settings


class OdooClient:
    """Reusable JSON-RPC client for Odoo CRUD operations."""

    def __init__(self):
        self.base_url = settings.BASE_URL
        self.database = settings.ODOO_DB
        self.username = settings.ODOO_USER
        self.password = settings.ODOO_PASSWORD

        self.url = f"{self.base_url}/jsonrpc"
        self.uid = None

    def _jsonrpc(self, service: str, method: str, args: list):
        """Send a JSON-RPC request to Odoo and return the result."""

        payload = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "service": service,
                "method": method,
                "args": args,
            },
        }

        response = requests.post(self.url, json=payload)
        result = response.json()

        if result.get("error"):
            error_msg = (
                result["error"].get("data", {}).get("message", "Unknown Odoo error")
            )
            raise Exception(f"Odoo API error: {error_msg}")

        return result.get("result")

    def authenticate(self):
        """Log in to Odoo via JSON-RPC and store the user ID."""

        self.uid = self._jsonrpc(
            "common",
            "authenticate",
            [self.database, self.username, self.password, {}],
        )

        if not self.uid:
            raise Exception(f"Authentication failed for {self.username}")

        return self.uid

    def create(self, model: str, values: dict) -> int:
        """Create a new record. Returns the new record ID."""

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
        """Read records by IDs. Returns list of dicts."""

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
        """Search for records matching a domain filter. Returns list of IDs."""

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
        """Update existing records. Returns True on success."""

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
        """Delete records. Returns True on success."""

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
        """Search and read in one call. Returns list of matching records."""

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
