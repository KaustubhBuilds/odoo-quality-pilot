import allure
from playwright.sync_api import Page, expect

from pages.base_page import BasePage


class ContactsPage(BasePage):
    """Page object for Odoo Contacts module."""

    def __init__(self, page: Page):
        super().__init__(page)

    @allure.step("Navigate to Contacts list")
    def go_to_contacts(self):
        """Navigate to contacts via Home Menu, then switch to list view."""
        self.page.get_by_title("Home Menu").click()
        self.page.get_by_role("menuitem", name="Contacts").first.click()
        self.page.wait_for_load_state("domcontentloaded")
        # Contacts defaults to kanban on fresh install — switch to list
        self.page.wait_for_selector(
            ".o_list_view, .o_kanban_view", timeout=self.timeout
        )
        if self.page.locator(".o_kanban_view").is_visible():
            self.page.locator(".o_switch_view.o_list").click()
            self.page.wait_for_selector(".o_list_view", timeout=self.timeout)

    @allure.step("Click New button")
    def click_new(self):
        self.page.get_by_role("button", name="New").click()
        self.page.get_by_role("radio", name="Individual").check()

    @allure.step("Fill contact name: {name}")
    def fill_name(self, name: str):
        self.page.get_by_role("textbox", name="e.g. Brandom Freeman").fill(name)

    @allure.step("Fill contact mobile: {mobile}")
    def fill_mobile(self, mobile: str):
        self.page.get_by_role("textbox", name="Mobile").fill(mobile)

    @allure.step("Fill contact email: {email}")
    def fill_email(self, email: str):
        self.page.get_by_role("textbox", name="Email").fill(email)

    @allure.step("Save contact")
    def save(self):
        import re

        self.page.get_by_role("textbox", name="e.g. Brandom Freeman").press("Enter")
        # Wait for URL to contain id= — confirms record was saved in database
        self.page.wait_for_url(re.compile(r".*id=\d+.*"), timeout=self.timeout)

    @allure.step("Search for contact: {query}")
    def search(self, query: str):
        self.page.get_by_role("searchbox", name="Search...").fill(query)
        self.page.keyboard.press("Enter")
        self.page.wait_for_load_state("domcontentloaded")

    @allure.step("Assert contact in list: {name}")
    def assert_contact_in_list(self, name: str):
        locator = self.page.locator(f".o_data_row:has-text('{name}')")
        expect(locator).to_be_visible(timeout=self.timeout)

    @allure.step("Assert contact NOT in list: {name}")
    def assert_contact_not_in_list(self, name: str):
        locator = self.page.locator(f".o_data_row:has-text('{name}')")
        expect(locator).not_to_be_visible(timeout=self.timeout)

    @allure.step("Open contact: {name}")
    def open_contact(self, name: str):
        self.page.get_by_role("cell", name=name).first.click()

    @allure.step("Assert form shows name: {name}")
    def assert_form_title(self, name: str):
        locator = self.page.get_by_role("textbox", name="e.g. Brandom Freeman")
        expect(locator).to_have_value(name, timeout=self.timeout)

    @allure.step("Delete current contact")
    def delete_contact(self):
        import re

        action_btn = (
            self.page.get_by_role("button").filter(has_text=re.compile(r"^$")).nth(2)
        )
        action_btn.wait_for(state="visible", timeout=self.timeout)
        action_btn.click()
        self.page.wait_for_timeout(500)
        delete_item = self.page.get_by_role("menuitem", name=" Delete")
        delete_item.wait_for(state="visible", timeout=self.timeout)
        delete_item.click()
        self.page.get_by_role("button", name="Delete").click()
        self.page.wait_for_load_state("domcontentloaded")

    @allure.step("Create contact setup helper")
    def create_contact(self, contact_data: dict):
        self.click_new()
        self.fill_name(contact_data["name"])
        self.fill_email(contact_data["email"])
        self.fill_mobile(contact_data["mobile"])
        self.save()
