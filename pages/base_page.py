import allure
from playwright.sync_api import Page, expect

from config.settings import settings


class BasePage:
    """Base class for all page objects. Common actions shared across pages."""

    def __init__(self, page: Page):
        self.page = page
        self.timeout = settings.TIMEOUT

    @allure.step("Navigate to {url}")
    def navigate(self, url: str):
        self.page.goto(url, timeout=self.timeout)

    @allure.step("Click element: {locator}")
    def click(self, locator: str):
        self.page.locator(locator).click(timeout=self.timeout)

    @allure.step("Fill field: {locator} with value")
    def fill(self, locator: str, value: str):
        self.page.locator(locator).fill(value)

    @allure.step("Assert element is visible: {locator}")
    def assert_visible(self, locator: str):
        expect(self.page.locator(locator)).to_be_visible(timeout=self.timeout)

    @allure.step("Assert element contains text: {expected}")
    def assert_text(self, locator: str, expected: str):
        expect(self.page.locator(locator)).to_contain_text(
            expected, timeout=self.timeout
        )

    @allure.step("Assert element is hidden: {locator}")
    def assert_hidden(self, locator: str):
        expect(self.page.locator(locator)).to_be_hidden(timeout=self.timeout)

    @allure.step("Get text from element: {locator}")
    def get_text(self, locator: str) -> str:
        return self.page.locator(locator).inner_text()

    @allure.step("Wait for URL to contain: {url_part}")
    def wait_for_url(self, url_part: str):
        self.page.wait_for_url(f"**{url_part}**", timeout=self.timeout)

    def take_screenshot(self, name: str = "screenshot"):
        """Capture screenshot and attach to Allure report."""

        allure.attach(
            self.page.screenshot(),
            name=name,
            attachment_type=allure.attachment_type.PNG,
        )
