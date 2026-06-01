import re

import allure
from playwright.sync_api import Page, expect

from pages.base_page import BasePage


class SalesPage(BasePage):
    """Page object for Odoo Sales module and quotation to order workflow."""

    def __init__(self, page: Page):
        super().__init__(page)

    @allure.step("Navigate to Sales Quotations list")
    def go_to_quotations(self):
        """Navigate to Sales via Home Menu. No hardcoded database IDs."""

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
        """Select first available customer from dropdown"""

        customer_combo = self.page.get_by_role(
            "combobox", name="Type to find a customer..."
        )
        customer_combo.click()
        self.page.wait_for_timeout(500)
        self.page.get_by_role("option").first.click()

    @allure.step("Add first available product")
    def add_product(self):
        """Add first available product to order lines"""

        self.page.get_by_role("button", name="Add a product").click()
        product_combo = self.page.get_by_role(
            "combobox", name="Type to find a product..."
        )
        product_combo.click()
        self.page.wait_for_timeout(500)
        self.page.get_by_role("option").first.click()

    @allure.step("Confirm quotation converts to Sales Order")
    def confirm_quotation(self):
        """Confirm quotation which converts it to a Sales Order."""

        self.page.get_by_role("button", name="Confirm", exact=True).click()
        self.page.wait_for_load_state("domcontentloaded")

    @allure.step("Cancel current Sales Order")
    def cancel_order(self):
        """Cancel order. Two-step: button click + modal confirmation."""

        self.page.get_by_role("button", name="Cancel").click()
        self.page.locator("#dialog_0").get_by_role(
            "button", name="Cancel", exact=True
        ).click()
        self.page.wait_for_load_state("domcontentloaded")

    @allure.step("Open quotation: {reference}")
    def open_quotation(self, reference: str):
        """Open a quotation by its reference number."""

        self.page.get_by_role("cell", name=reference).first.click()
        self.page.wait_for_load_state("domcontentloaded")

    @allure.step("Assert status shows: {status}")
    def assert_status(self, status: str):
        """Verify the status badge shows expected value."""

        status_locator = self.page.locator(
            f".o_arrow_button_current:has-text('{status}')"
        )
        expect(status_locator).to_be_visible(timeout=self.timeout)

    @allure.step("Assert Delivery button is visible")
    def assert_delivery_button_visible(self):
        """Verify delivery button appears after confirmation."""

        delivery_btn = self.page.get_by_role(
            "button", name=re.compile(r"\d+ Delivery", re.IGNORECASE)
        )
        expect(delivery_btn).to_be_visible(timeout=self.timeout)
