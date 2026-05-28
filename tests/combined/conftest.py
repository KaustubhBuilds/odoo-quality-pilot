"""
Combined test fixtures.

Provides an authenticated API client alongside the
logged_in_page fixture from root conftest.
"""

import pytest

from services.odoo_client import OdooClient


@pytest.fixture(scope="session")
def api_client():
    """Authenticated Odoo API client for combined tests."""
    client = OdooClient()
    client.authenticate()
    return client
