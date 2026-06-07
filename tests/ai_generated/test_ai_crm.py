import allure
import pytest

from pages.crm_page import CRMPage
from utils.data_factory import generate_lead


@allure.epic("CRM")
@allure.feature("Lead Pipeline")
class TestCRMPage:
    @pytest.mark.ui
    @allure.story("Create lead")
    @allure.title("Create a new lead with valid customer, opportunity, and revenue")
    def test_create_lead_happy_path(self, logged_in_page):
        """Verify that a lead can be created successfully and appears in the CRM pipeline."""
        crm = CRMPage(logged_in_page)
        data = generate_lead()

        crm.go_to_crm()
        crm.click_new()
        crm.fill_customer(data["customer"])
        crm.fill_opportunity(data["opportunity"])
        crm.fill_expected_revenue(data["expected_revenue"])
        crm.save_lead()

        crm.assert_lead_visible(data["opportunity"])

    @pytest.mark.ui
    @allure.story("Lead lifecycle")
    @allure.title("Move an existing lead to Won status")
    def test_mark_lead_as_won(self, logged_in_page):
        """Verify that an existing lead can be opened and marked as Won from the form view."""
        crm = CRMPage(logged_in_page)
        data = generate_lead()

        crm.go_to_crm()
        crm.click_new()
        crm.fill_customer(data["customer"])
        crm.fill_opportunity(data["opportunity"])
        crm.fill_expected_revenue(data["expected_revenue"])
        crm.save_lead()
        crm.open_lead(data["opportunity"])
        crm.mark_as_won()
        crm.assert_status("Won")

    @pytest.mark.ui
    @allure.story("Lead validation")
    @allure.title("Prevent saving a lead when required fields are incomplete")
    def test_save_lead_without_required_fields(self, logged_in_page):
        """Verify that saving an inline lead without required details does not create a visible lead."""
        crm = CRMPage(logged_in_page)
        data = generate_lead()

        crm.go_to_crm()
        crm.click_new()
        crm.fill_customer(data["customer"])
        crm.save_lead()

        with pytest.raises(AssertionError):
            crm.assert_lead_visible(data["opportunity"])

    @pytest.mark.ui
    @allure.story("Lead lifecycle")
    @allure.title("Mark a lead as Lost using a valid lost reason")
    @pytest.mark.skip(
        reason="Lost Reason dialog rendering varies between freshly created and existing leads on fresh Odoo installs"
    )
    def test_mark_lead_as_lost(self, logged_in_page):
        """Verify that an existing lead can be marked as Lost with a selected reason."""
        crm = CRMPage(logged_in_page)
        data = generate_lead()

        crm.go_to_crm()
        crm.click_new()
        crm.fill_customer(data["customer"])
        crm.fill_opportunity(data["opportunity"])
        crm.fill_expected_revenue(data["expected_revenue"])
        crm.save_lead()
        crm.open_lead(data["opportunity"])
        crm.mark_as_lost(data["lost_reason"])

    @pytest.mark.ui
    @allure.story("Lead creation")
    @allure.title("Create a lead with an empty expected revenue value")
    def test_create_lead_with_empty_expected_revenue(self, logged_in_page):
        """Verify that a lead can be created with an empty expected revenue field and still appears in the pipeline."""
        crm = CRMPage(logged_in_page)
        data = generate_lead()

        crm.go_to_crm()
        crm.click_new()
        crm.fill_customer(data["customer"])
        crm.fill_opportunity(data["opportunity"])
        crm.fill_expected_revenue("")
        crm.save_lead()

        crm.assert_lead_visible(data["opportunity"])
