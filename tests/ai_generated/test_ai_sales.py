import allure
import pytest

from pages.sales_page import SalesPage
from utils.data_factory import Faker


@pytest.mark.ui
@allure.epic("Odoo UI")
@allure.feature("Sales Quotations")
class TestSalesPage:
    """UI tests for the Sales module quotation workflow."""

    def _create_sales_page(self, logged_in_page):
        return SalesPage(logged_in_page)

    @pytest.mark.ui
    @allure.story("Quotation creation and confirmation")
    @allure.title("Happy path: create a quotation, confirm it, and verify delivery")
    def test_create_confirm_quotation_happy_path(self, logged_in_page):
        """Verify a user can open Sales, create a quotation, confirm it, and see the delivery action."""
        sales_page = self._create_sales_page(logged_in_page)

        sales_page.go_to_quotations()
        sales_page.click_new()

        sales_page.select_customer()
        sales_page.add_product()

        sales_page.confirm_quotation()

        sales_page.assert_status("Sales Order")
        sales_page.assert_delivery_button_visible()

    @pytest.mark.ui
    @allure.story("Quotation workflow validation")
    @allure.title("Negative path: opening a non-existent quotation should fail")
    def test_open_non_existent_quotation_negative_path(self, logged_in_page):
        """Verify that attempting to open a quotation with a random non-existent reference fails."""
        sales_page = self._create_sales_page(logged_in_page)
        faker = Faker()
        invalid_reference = f"S{faker.random_int(min=100000, max=999999)}"

        sales_page.go_to_quotations()

        with pytest.raises(Exception):
            sales_page.open_quotation(invalid_reference)

    @pytest.mark.ui
    @allure.story("Quotation workflow edge cases")
    @allure.title(
        "Edge case: create quotation with minimal available data and cancel it"
    )
    def test_confirm_and_cancel_quotation_edge_case(self, logged_in_page):
        """Verify that a quotation can be confirmed and then canceled without relying on specific records."""
        sales_page = self._create_sales_page(logged_in_page)

        sales_page.go_to_quotations()
        sales_page.click_new()

        sales_page.select_customer()
        sales_page.add_product()
        sales_page.confirm_quotation()

        sales_page.assert_status("Sales Order")
        sales_page.cancel_order()
        sales_page.assert_status("Cancelled")
