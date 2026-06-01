import allure
from playwright.sync_api import Page, expect

from pages.base_page import BasePage


class CRMPage(BasePage):
    """Page object for Odoo CRM module — lead pipeline workflow."""

    def __init__(self, page: Page):
        super().__init__(page)

    @allure.step("Navigate to CRM pipeline")
    def go_to_crm(self):
        """Navigate to CRM via Home Menu."""

        self.page.get_by_title("Home Menu").click()
        self.page.get_by_role("menuitem", name="CRM").click()
        self.page.wait_for_load_state("domcontentloaded")

    @allure.step("Click New lead button")
    def click_new(self):
        """Open inline lead creation form in the New column."""

        self.page.get_by_role("button", name="New").click()
        self.page.wait_for_timeout(500)

    @allure.step("Fill customer: {customer_name}")
    def fill_customer(self, customer_name: str):
        """Type customer name and select the Create option."""

        customer_combo = self.page.get_by_role("combobox").first
        customer_combo.click()
        customer_combo.fill(customer_name)
        self.page.wait_for_timeout(500)
        # Select the Create option (creates customer if new)
        self.page.get_by_role("option", name=f'Create "{customer_name}"').click()

    @allure.step("Fill opportunity title: {title}")
    def fill_opportunity(self, title: str):
        """Fills the Opportunity title field."""

        self.page.get_by_role("textbox", name="Opportunity").fill(title)

    @allure.step("Fill expected revenue: {amount}")
    def fill_expected_revenue(self, amount: str):
        """Fills the Expected Revenue field."""

        self.page.get_by_role("textbox", name="Expected Revenue").fill(amount)

    @allure.step("Save lead click Add button")
    def save_lead(self):
        """Save lead via Add button. exact=True avoids ambiguous match."""

        self.page.get_by_role("button", name="Add", exact=True).click()
        self.page.wait_for_load_state("domcontentloaded")

    @allure.step("Open lead: {title}")
    def open_lead(self, title: str):
        """Click on lead in Kanban view to open its full form."""

        self.page.get_by_text(title).first.click()
        self.page.wait_for_load_state("domcontentloaded")

    @allure.step("Change lead stage to: {stage_name}")
    def change_stage(self, stage_name: str):
        """Change pipeline stage using the radio button selectors
        at the top of the lead form."""

        self.page.get_by_role("radio", name=stage_name).click()
        self.page.wait_for_load_state("domcontentloaded")

    @allure.step("Mark lead as Won")
    def mark_as_won(self):
        """Click Won button on the lead form."""

        self.page.get_by_role("button", name="Won").click()
        self.page.wait_for_load_state("domcontentloaded")

    @allure.step("Mark lead as Lost with reason: {reason}")
    def mark_as_lost(self, reason: str):
        """
        Three-step Lost flow:
        1. Click Lost button (opens modal)
        2. Select reason from dropdown
        3. Click 'Mark as Lost' to confirm
        """
        self.page.get_by_role("button", name="Lost").click()
        self.page.wait_for_timeout(500)
        self.page.get_by_role("combobox", name="Lost Reason").click()
        self.page.get_by_role("option", name=reason).click()
        self.page.get_by_role("button", name="Mark as Lost").click()
        self.page.wait_for_load_state("domcontentloaded")

    @allure.step("Assert lead is visible: {title}")
    def assert_lead_visible(self, title: str):
        """Verify lead appears in Kanban view."""

        locator = self.page.get_by_text(title).first
        expect(locator).to_be_visible(timeout=self.timeout)

    @allure.step("Assert status: {status}")
    def assert_status(self, status: str):
        """Verify the status badge shows expected value."""

        status_locator = self.page.locator(
            f".o_arrow_button_current:has-text('{status}')"
        )
        expect(status_locator).to_be_visible(timeout=self.timeout)
