"""
Combined API + UI tests.

The professional hybrid pattern:
- Setup data via API (fast — milliseconds)
- Verify in UI (only when browser check is needed)
- Cleanup via API (fast — no browser interaction)
"""

import allure
import pytest

from pages.contacts_page import ContactsPage
from utils.data_factory import generate_contact, generate_lead


@allure.epic("Combined Testing")
@allure.feature("API Setup + UI Verification")
class TestHybrid:
    @pytest.mark.combined
    @allure.story("Contact created via API appears in UI")
    @allure.title("API-created contact is visible in Contacts list")
    def test_api_contact_visible_in_ui(self, api_client, logged_in_page):
        """
        1. Create contact via API (instant)
        2. Use ContactsPage to navigate and search (verified selectors)
        3. Verify it appears in the list
        4. Cleanup via API (instant)
        """
        data = generate_contact()

        # --- API SETUP ---
        contact_id = api_client.create(
            "res.partner",
            {"name": data["name"], "email": data["email"]},
        )

        # --- UI VERIFICATION ---
        contacts = ContactsPage(logged_in_page)
        contacts.go_to_contacts()
        contacts.search(data["name"])
        contacts.assert_contact_in_list(data["name"])

        # --- API CLEANUP ---
        api_client.unlink("res.partner", [contact_id])

    @pytest.mark.combined
    @allure.story("Lead created via API appears in CRM pipeline")
    @allure.title("API-created lead is visible in CRM Kanban")
    def test_api_lead_visible_in_crm(self, api_client, logged_in_page):
        """
        Create a CRM lead via API, verify it appears in
        the Kanban pipeline in the browser.
        """
        data = generate_lead()

        # --- API SETUP ---
        lead_id = api_client.create(
            "crm.lead",
            {
                "name": data["opportunity"],
                "expected_revenue": float(data["expected_revenue"]),
            },
        )

        # --- UI VERIFICATION ---
        logged_in_page.get_by_title("Home Menu").click()
        logged_in_page.get_by_role("menuitem", name="CRM").click()
        logged_in_page.wait_for_load_state("domcontentloaded")
        logged_in_page.wait_for_timeout(1000)

        from playwright.sync_api import expect

        expect(logged_in_page.get_by_text(data["opportunity"]).first).to_be_visible(
            timeout=10000
        )

        # --- API CLEANUP ---
        api_client.unlink("crm.lead", [lead_id])

    @pytest.mark.combined
    @allure.story("UI-created contact verifiable via API")
    @allure.title("Contact created in browser exists in API")
    def test_ui_contact_verified_via_api(self, api_client, logged_in_page):
        """
        1. Create contact via UI using ContactsPage
        2. Navigate back to list (triggers full save in Odoo)
        3. Verify via API that the contact exists in the database
        4. Cleanup via API
        """
        data = generate_contact()

        # --- UI ACTION ---
        contacts = ContactsPage(logged_in_page)
        contacts.go_to_contacts()
        contacts.create_contact(data)

        # Navigate back to list — this forces Odoo to fully commit
        contacts.go_to_contacts()
        contacts.search(data["name"])
        contacts.assert_contact_in_list(data["name"])

        # --- API VERIFICATION ---
        found = api_client.search("res.partner", [("name", "=", data["name"])])
        assert len(found) > 0, f"Contact '{data['name']}' not found via API"

        result = api_client.read("res.partner", found, ["name", "email"])
        assert result[0]["name"] == data["name"]
        assert result[0]["email"] == data["email"]

        # --- API CLEANUP ---
        api_client.unlink("res.partner", found)
