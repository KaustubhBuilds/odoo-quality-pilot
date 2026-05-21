import re

import allure
from playwright.sync_api import Page, expect

from pages.base_page import BasePage


class SalesPage(BasePage):
    """
    Page object for Odoo Sales module.
    Tests the quotation sales order workflow.
    All selectors verified from Playwright Inspector recording.
    """

    def __init__(self, page: Page):
        super().__init__(page)

    @allure.step("Navigate to Sales Quotations list")
    def go_to_quotations(self):
        """
        Navigate via menu: Home Menu - Sales.
        Professional approach - no database IDs.
        Works across any Odoo environment.
        """
        self.page.get_by_title("Home Menu").click()
        self.page.get_by_role("menuitem", name="Sales").click()
        self.page.wait_for_load_state("domcontentloaded")

    @allure.step("Click New quotation button")
    def click_new(self):
        """Opens blank quotation form."""
        self.page.get_by_role("button", name="New").click()
        self.page.wait_for_load_state("domcontentloaded")

    @allure.step("Select first available customer")
    def select_customer(self):
        """
        Open customer dropdown and select the first available customer.
        Test does not depend on specific customer data existing.
        Tests the WORKFLOW, not specific data.
        """
        customer_combo = self.page.get_by_role(
            "combobox", name="Type to find a customer..."
        )
        customer_combo.click()
        self.page.wait_for_timeout(500)
        self.page.get_by_role("option").first.click()

    @allure.step("Add first available product")
    def add_product(self):
        """
        Click 'Add a product' then select first available product.
        Test does not depend on specific products existing.
        """
        self.page.get_by_role("button", name="Add a product").click()
        product_combo = self.page.get_by_role(
            "combobox", name="Type to find a product..."
        )
        product_combo.click()
        self.page.wait_for_timeout(500)
        self.page.get_by_role("option").first.click()

    @allure.step("Confirm quotation — converts to Sales Order")
    def confirm_quotation(self):
        """
        Click Confirm button on the quotation form.
        After confirmation, the quotation becomes a Sales Order.
        """
        self.page.get_by_role("button", name="Confirm").click()
        self.page.wait_for_load_state("domcontentloaded")

    @allure.step("Cancel current Sales Order")
    def cancel_order(self):
        """
        Cancel a confirmed Sales Order.
        Two-step flow: click Cancel → confirm in modal.
        Uses exact=True for the modal button to avoid wrong match.
        """
        self.page.get_by_role("button", name="Cancel").click()
        self.page.locator("#dialog_0").get_by_role(
            "button", name="Cancel", exact=True
        ).click()
        self.page.wait_for_load_state("domcontentloaded")

    @allure.step("Open quotation: {reference}")
    def open_quotation(self, reference: str):
        """
        Open a quotation from the list by its S00XXX reference.
        Uses cell role — same pattern as Contacts.
        """
        self.page.get_by_role("cell", name=reference).first.click()
        self.page.wait_for_load_state("domcontentloaded")

    @allure.step("Assert status shows: {status}")
    def assert_status(self, status: str):
        """
        Verify status badge shows expected value.
        """
        status_locator = self.page.locator(
            f".o_arrow_button_current:has-text('{status}')"
        )
        expect(status_locator).to_be_visible(timeout=self.timeout)

    @allure.step("Assert Delivery button is visible")
    def assert_delivery_button_visible(self):
        """
        After confirming a quotation, Odoo creates a delivery.
        Reliable indicator of successful confirmation.
        """
        delivery_btn = self.page.get_by_role(
            "button", name=re.compile(r"\d+ Delivery", re.IGNORECASE)
        )
        expect(delivery_btn).to_be_visible(timeout=self.timeout)
