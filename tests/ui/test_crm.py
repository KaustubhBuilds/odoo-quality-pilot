import allure
import pytest

from pages.crm_page import CRMPage
from utils.data_factory import generate_lead


@allure.epic("CRM Management")
@allure.feature("Lead Pipeline")
class TestCRM:
    @pytest.mark.ui
    @allure.story("Create lead")
    @allure.title("Create a new lead in the pipeline")
    def test_create_lead(self, logged_in_page):
        lead_data = generate_lead()
        crm = CRMPage(logged_in_page)

        crm.go_to_crm()
        crm.click_new()
        crm.fill_customer(lead_data["customer"])
        crm.fill_opportunity(lead_data["opportunity"])
        crm.fill_expected_revenue(lead_data["expected_revenue"])
        crm.save_lead()

        crm.assert_lead_visible(lead_data["opportunity"])

    @pytest.mark.ui
    @allure.story("Change pipeline stage")
    @allure.title("Move lead from New to Qualified stage")
    def test_change_lead_stage(self, logged_in_page):
        lead_data = generate_lead()
        crm = CRMPage(logged_in_page)

        crm.go_to_crm()
        crm.click_new()
        crm.fill_customer(lead_data["customer"])
        crm.fill_opportunity(lead_data["opportunity"])
        crm.fill_expected_revenue(lead_data["expected_revenue"])
        crm.save_lead()

        crm.open_lead(lead_data["opportunity"])
        crm.change_stage("Qualified")

    @pytest.mark.smoke
    @pytest.mark.ui
    @allure.story("Mark as Won")
    @allure.title("Lead can be marked as Won")
    def test_mark_lead_as_won(self, logged_in_page):
        lead_data = generate_lead()
        crm = CRMPage(logged_in_page)

        crm.go_to_crm()
        crm.click_new()
        crm.fill_customer(lead_data["customer"])
        crm.fill_opportunity(lead_data["opportunity"])
        crm.fill_expected_revenue(lead_data["expected_revenue"])
        crm.save_lead()

        crm.open_lead(lead_data["opportunity"])
        crm.mark_as_won()

    @pytest.mark.ui
    @allure.story("Mark as Lost")
    @allure.title("Lead can be marked as Lost with required reason")
    @pytest.mark.skip(
        reason="Lost Reason dialog rendering varies between freshly created and existing leads on fresh Odoo installs"
    )
    def test_mark_lead_as_lost(self, logged_in_page):
        lead_data = generate_lead()
        crm = CRMPage(logged_in_page)

        crm.go_to_crm()
        crm.click_new()
        crm.fill_customer(lead_data["customer"])
        crm.fill_opportunity(lead_data["opportunity"])
        crm.fill_expected_revenue(lead_data["expected_revenue"])
        crm.save_lead()

        crm.open_lead(lead_data["opportunity"])
        crm.mark_as_lost(lead_data["lost_reason"])

    @pytest.mark.ui
    @allure.story("Full pipeline journey")
    @allure.title("Lead progresses through full pipeline to Won")
    def test_full_pipeline_flow(self, logged_in_page):
        lead_data = generate_lead()
        crm = CRMPage(logged_in_page)

        # Create
        crm.go_to_crm()
        crm.click_new()
        crm.fill_customer(lead_data["customer"])
        crm.fill_opportunity(lead_data["opportunity"])
        crm.fill_expected_revenue(lead_data["expected_revenue"])
        crm.save_lead()

        # Move to Qualified
        crm.open_lead(lead_data["opportunity"])
        crm.change_stage("Qualified")

        # Mark as Won
        crm.mark_as_won()
