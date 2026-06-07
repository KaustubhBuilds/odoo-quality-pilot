import allure
import pytest

from pages.sales_page import SalesPage


@allure.epic("Sales Management")
@allure.feature("Sales Order Workflow")
class TestSales:
    @pytest.mark.ui
    @allure.story("Create quotation")
    @allure.title("Create a new quotation with customer and product")
    def test_create_quotation(self, logged_in_page):
        sales = SalesPage(logged_in_page)

        sales.go_to_quotations()
        sales.click_new()
        sales.select_customer()
        sales.add_product()

        sales.assert_status("Quotation")

    @pytest.mark.smoke
    @pytest.mark.ui
    @allure.story("Confirm quotation to Sales Order")
    @allure.title("Confirming a quotation converts it to Sales Order")
    @pytest.mark.skip(
        reason="Delivery button appearance depends on first product type in demo data "
        "(storable vs service). Demo data ordering varies on fresh installs."
    )
    def test_confirm_quotation_to_order(self, logged_in_page):
        sales = SalesPage(logged_in_page)

        sales.go_to_quotations()
        sales.click_new()
        sales.select_customer()
        sales.add_product()
        sales.confirm_quotation()

        sales.assert_status("Sales Order")
        sales.assert_delivery_button_visible()

    @pytest.mark.ui
    @allure.story("Multi-product orders")
    @allure.title("Quotation accepts multiple products")
    def test_add_multiple_products(self, logged_in_page):
        sales = SalesPage(logged_in_page)

        sales.go_to_quotations()
        sales.click_new()
        sales.select_customer()
        sales.add_product()
        sales.add_product()

        sales.assert_status("Quotation")

    @pytest.mark.ui
    @allure.story("Cancel sales order")
    @allure.title("Confirmed Sales Order can be cancelled")
    @pytest.mark.skip(
        reason="Cancel flow requires customer email/phone validation that varies based on customer demo data"
    )
    def test_cancel_sales_order(self, logged_in_page):
        sales = SalesPage(logged_in_page)

        sales.go_to_quotations()
        sales.click_new()
        sales.select_customer()
        sales.add_product()
        sales.confirm_quotation()
        sales.assert_status("Sales Order")

        sales.cancel_order()

        sales.assert_status("Cancelled")

    @pytest.mark.ui
    @allure.story("Form validation")
    @allure.title("Cannot confirm quotation without customer")
    def test_quotation_validation(self, logged_in_page):
        sales = SalesPage(logged_in_page)

        sales.go_to_quotations()
        sales.click_new()

        sales.confirm_quotation()

        sales.assert_status("Quotation")
