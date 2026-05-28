"""
API tests for Odoo Contacts (res.partner model).

These test the same CRUD operations as the UI tests,
but through the API no browser, runs in seconds.

Each test creates its own data and cleans up after itself.
"""

import allure
import pytest

from utils.data_factory import generate_contact


@allure.epic("API Testing")
@allure.feature("Contacts API")
class TestContactsAPI:
    @pytest.mark.api
    @allure.story("Create contact via API")
    @allure.title("Create a contact and verify it returns a valid ID")
    def test_create_contact_via_api(self, api_client):
        """Create a contact via API. Verify we get a valid ID back."""
        data = generate_contact()

        contact_id = api_client.create(
            "res.partner", {"name": data["name"], "email": data["email"]}
        )

        assert isinstance(contact_id, int), "Expected an integer ID"
        assert contact_id > 0, "ID should be positive"

        # Cleanup
        api_client.unlink("res.partner", [contact_id])

    @pytest.mark.api
    @allure.story("Read contact via API")
    @allure.title("Create a contact then read it back and verify fields")
    def test_read_contact_via_api(self, api_client):
        """Create a contact, read it back, verify the data matches."""
        data = generate_contact()

        # Create
        contact_id = api_client.create(
            "res.partner",
            {"name": data["name"], "email": data["email"]},
        )

        # Read back
        contacts = api_client.read("res.partner", [contact_id], ["name", "email"])

        # Verify
        assert len(contacts) == 1, "Should return exactly one contact"
        assert contacts[0]["name"] == data["name"]
        assert contacts[0]["email"] == data["email"]

        # Cleanup
        api_client.unlink("res.partner", [contact_id])

    @pytest.mark.api
    @allure.story("Update contact via API")
    @allure.title("Create a contact, update its name, verify the change")
    def test_update_contact_via_api(self, api_client):
        """Create, update, then read back to verify the update worked."""
        data = generate_contact()
        new_name = "Updated " + data["name"]

        # Create
        contact_id = api_client.create("res.partner", {"name": data["name"]})

        # Update
        result = api_client.write("res.partner", [contact_id], {"name": new_name})
        assert result is True, "Write should return True"

        # Verify update
        contacts = api_client.read("res.partner", [contact_id], ["name"])
        assert contacts[0]["name"] == new_name

        # Cleanup
        api_client.unlink("res.partner", [contact_id])

    @pytest.mark.api
    @allure.story("Delete contact via API")
    @allure.title("Create a contact, delete it, verify it is gone")
    def test_delete_contact_via_api(self, api_client):
        """Create, delete, then search to confirm it no longer exists."""
        data = generate_contact()

        # Create
        contact_id = api_client.create("res.partner", {"name": data["name"]})

        # Delete
        result = api_client.unlink("res.partner", [contact_id])
        assert result is True, "Unlink should return True"

        # Verify deleted — search should return empty
        found = api_client.search("res.partner", [("id", "=", contact_id)])
        assert len(found) == 0, "Deleted contact should not be found"

    @pytest.mark.api
    @allure.story("Search contacts via API")
    @allure.title("Create a contact and find it via search")
    def test_search_contact_via_api(self, api_client):
        """Create a contact with a unique name, search for it, verify found."""
        data = generate_contact()

        # Create
        contact_id = api_client.create("res.partner", {"name": data["name"]})

        # Search by exact name
        found = api_client.search("res.partner", [("name", "=", data["name"])])

        # Verify
        assert contact_id in found, "Created contact should appear in search"

        # Cleanup
        api_client.unlink("res.partner", [contact_id])
