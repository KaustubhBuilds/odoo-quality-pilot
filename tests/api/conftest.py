"""
API test fixtures.

Provides an authenticated OdooClient for all API tests.
The client authenticates once per test session (not per test)
for efficiency API auth is stateless so this is safe.
"""

import pytest

from services.odoo_client import OdooClient


@pytest.fixture(scope="session")
def api_client():
    """
    Authenticated Odoo API client.
    Shared across all API tests in the session.
    """
    client = OdooClient()
    client.authenticate()
    return client
