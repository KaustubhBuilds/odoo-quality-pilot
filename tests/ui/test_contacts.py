import allure
import pytest

from pages.contacts_page import ContactsPage
from utils.data_factory import generate_contact


@allure.epic("Contacts Management")
@allure.feature("Contact CRUD")
class TestContacts:
    @pytest.mark.ui
    @allure.story("Create contact")
    @allure.title("Create a new contact and verify it appears in list")
    def test_create_contact(self, logged_in_page):
        contact_data = generate_contact()
        contacts = ContactsPage(logged_in_page)

        contacts.go_to_contacts()
        contacts.click_new()
        contacts.fill_name(contact_data["name"])
        contacts.fill_email(contact_data["email"])
        contacts.fill_mobile(contact_data["mobile"])
        contacts.save()

        contacts.go_to_contacts()
        contacts.search(contact_data["name"])
        contacts.assert_contact_in_list(contact_data["name"])

    @pytest.mark.ui
    @allure.story("Read contact")
    @allure.title("Search for a contact and verify correct result")
    def test_search_contact(self, logged_in_page):
        contact_data = generate_contact()
        contacts = ContactsPage(logged_in_page)

        contacts.go_to_contacts()
        contacts.create_contact(contact_data)

        contacts.go_to_contacts()
        contacts.search(contact_data["name"])
        contacts.assert_contact_in_list(contact_data["name"])

    @pytest.mark.ui
    @allure.story("Update contact")
    @allure.title("Edit contact name and verify update is saved")
    def test_edit_contact(self, logged_in_page):
        contact_data = generate_contact()
        updated_data = generate_contact()
        contacts = ContactsPage(logged_in_page)

        contacts.go_to_contacts()
        contacts.create_contact(contact_data)

        contacts.go_to_contacts()
        contacts.search(contact_data["name"])
        contacts.open_contact(contact_data["name"])

        contacts.fill_name(updated_data["name"])
        contacts.save()

        contacts.assert_form_title(updated_data["name"])

    @pytest.mark.skip(
        reason="Form-view delete behavior varies between fresh and stateful Odoo installs. "
        "Delete is covered by tests/api/test_contacts_api.py::test_delete_contact_via_api"
    )
    @pytest.mark.ui
    @allure.story("Delete contact")
    @allure.title("Delete a contact and verify it is removed from list")
    @pytest.mark.skip(
        reason="Form-view delete behavior varies between fresh and stateful Odoo installs. "
        "Delete is covered by tests/api/test_contacts_api.py::test_delete_contact_via_api"
    )
    def test_delete_contact(self, logged_in_page):
        contact_data = generate_contact()
        contacts = ContactsPage(logged_in_page)

        contacts.go_to_contacts()
        contacts.create_contact(contact_data)

        contacts.go_to_contacts()
        contacts.search(contact_data["name"])
        contacts.open_contact(contact_data["name"])

        contacts.delete_contact()

        contacts.go_to_contacts()
        contacts.search(contact_data["name"])
        contacts.assert_contact_not_in_list(contact_data["name"])
