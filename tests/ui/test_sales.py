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
        reason=(
            "v1.0.2 attempted API customer fixture (customer_with_contact_info) to "
            "replace demo data dependency. Customer creation + selection works, but "
            "cancel action does not complete for API-created customers even with "
            "email+phone. Form Cancel button click fires correctly (verified via "
            "DevTools: 1 match, visible, name='action_cancel'), order is in 'sale' "
            "state, but no confirmation dialog appears and status does not transition "
            "to 'cancel'. Root cause likely involves mail follower subscription "
            "(message_subscribe) which UI-created customers get automatically but "
            "API-created ones do not. Deferred to v1.0.3."
        )
    )
    def test_cancel_sales_order(self, logged_in_page, customer_with_contact_info):
        sales = SalesPage(logged_in_page)

        sales.go_to_quotations()
        sales.click_new()
        sales.select_customer_by_name(customer_with_contact_info["name"])
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
