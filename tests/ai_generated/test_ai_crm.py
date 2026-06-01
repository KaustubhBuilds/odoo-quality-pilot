import allure
import pytest
from faker import Faker

from pages.crm_page import CRMPage
from utils.data_factory import Faker as DataFaker

fake = Faker()


@pytest.mark.ui
@allure.epic("CRM")
@allure.feature("Lead pipeline")
@allure.story("Create and manage leads")
@allure.title("Happy path: create a new CRM lead and verify it appears in the pipeline")
def test_create_new_lead_happy_path_logged_in_page(logged_in_page):
    """
    Verify that a user can create a new CRM lead with valid data and see it
    displayed in the pipeline after saving.
    """
    crm_page = CRMPage(logged_in_page)

    customer_name = DataFaker.customer_name()
    opportunity_title = fake.sentence(nb_words=4).rstrip(".")
    expected_revenue = str(fake.random_int(min=1000, max=99999))

    crm_page.go_to_crm()
    crm_page.click_new()
    crm_page.fill_customer(customer_name)
    crm_page.fill_opportunity(opportunity_title)
    crm_page.fill_expected_revenue(expected_revenue)
    crm_page.save_lead()

    crm_page.assert_lead_visible(opportunity_title)


@pytest.mark.ui
@allure.epic("CRM")
@allure.feature("Lead pipeline")
@allure.story("Create and manage leads")
@allure.title(
    "Negative path: create lead with invalid revenue and verify validation prevents save"
)
def test_create_lead_invalid_expected_revenue_logged_in_page(logged_in_page):
    """
    Verify that the CRM lead form does not accept a non-numeric expected revenue
    value and the lead is not created successfully.
    """
    crm_page = CRMPage(logged_in_page)

    customer_name = DataFaker.customer_name()
    opportunity_title = fake.sentence(nb_words=3).rstrip(".")
    invalid_revenue = fake.word()

    crm_page.go_to_crm()
    crm_page.click_new()
    crm_page.fill_customer(customer_name)
    crm_page.fill_opportunity(opportunity_title)
    crm_page.fill_expected_revenue(invalid_revenue)

    with pytest.raises(AssertionError):
        crm_page.save_lead()
        crm_page.assert_lead_visible(opportunity_title)


@pytest.mark.ui
@allure.epic("CRM")
@allure.feature("Lead pipeline")
@allure.story("Create and manage leads")
@allure.title(
    "Edge case: create lead with minimal boundary data and verify pipeline accepts it"
)
def test_create_lead_with_minimum_boundary_values_logged_in_page(logged_in_page):
    """
    Verify that the CRM lead form accepts minimal valid boundary data such as
    a one-character opportunity title and a minimum revenue value.
    """
    crm_page = CRMPage(logged_in_page)

    customer_name = DataFaker.customer_name()
    opportunity_title = "A"
    expected_revenue = "0"

    crm_page.go_to_crm()
    crm_page.click_new()
    crm_page.fill_customer(customer_name)
    crm_page.fill_opportunity(opportunity_title)
    crm_page.fill_expected_revenue(expected_revenue)
    crm_page.save_lead()

    crm_page.assert_lead_visible(opportunity_title)
