import allure
import pytest
from playwright.sync_api import sync_playwright

from config.settings import settings


@pytest.fixture(scope="session")
def browser_instance():
    """Launch browser once for the entire test session."""

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            headless=settings.HEADLESS,
            slow_mo=settings.SLOW_MO,
        )
        yield browser
        browser.close()


@pytest.fixture(scope="function")
def page(browser_instance):
    """Fresh browser context per test which ensures test isolation."""

    context = browser_instance.new_context(
        base_url=settings.BASE_URL,
        viewport={"width": 1920, "height": 1080},
    )
    page = context.new_page()
    yield page
    context.close()


@pytest.fixture(scope="function")
def logged_in_page(page):
    """Pre-authenticated page. Logs in before each test."""
    # Auto-dismiss Odoo onboarding tours on every page load
    page.add_init_script("""
        const observer = new MutationObserver(() => {
            document.querySelectorAll(
                '.o_tour_pointer, .o_tour_pointer_tip'
            ).forEach(el => el.remove());
        });
        if (document.body) {
            observer.observe(document.body, { childList: true, subtree: true });
        } else {
            document.addEventListener('DOMContentLoaded', () => {
                observer.observe(document.body, { childList: true, subtree: true });
            });
        }
    """)
    from pages.login_page import LoginPage

    login = LoginPage(page)
    login.open()
    login.login(settings.ODOO_USER, settings.ODOO_PASSWORD)
    login.assert_logged_in()
    yield page


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Auto-capture screenshot on test failure for Allure report."""

    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page_fixture = item.funcargs.get("page") or item.funcargs.get("logged_in_page")
        if page_fixture:
            allure.attach(
                page_fixture.screenshot(),
                name="failure_screenshot",
                attachment_type=allure.attachment_type.PNG,
            )
