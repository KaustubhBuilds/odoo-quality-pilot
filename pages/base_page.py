import allure
from playwright.sync_api import Page, expect

from config.settings import settings


class BasePage:
    """
    Parent class for all page objects.
    Contains common actions used across every page.
    All page objects inherit from this class.
    """

    def __init__(self, page: Page):
        """
        Every page object receives a Playwright Page object.
        We store it as self.page so all methods can use it.
        self.timeout comes from settings never hardcoded.
        """
        self.page = page
        self.timeout = settings.TIMEOUT

    @allure.step("Navigate to {url}")
    def navigate(self, url: str):
        """
        Navigate to a URL.
        The @allure.step decorator automatically adds this
        action as a named step in the Allure report.
        You see exactly what the test did, in order.
        """
        self.page.goto(url, timeout=self.timeout)

    @allure.step("Click element: {locator}")
    def click(self, locator: str):
        """
        Click any element by its locator.
        We never call page.click() directly in tests.
        Always go through this method.
        This means retry logic, logging, or waits can be
        added here once and apply to every click everywhere.
        """
        self.page.locator(locator).click(timeout=self.timeout)

    @allure.step("Fill field: {locator} with value")
    def fill(self, locator: str, value: str):
        """
        Clear a field and type a value into it.
        fill() replaces whatever is there — safer than type().
        """
        self.page.locator(locator).fill(value)

    @allure.step("Assert element is visible: {locator}")
    def assert_visible(self, locator: str):
        """
        Assert that an element is visible on the page.
        Uses Playwright's expect() which has built-in
        auto-waiting it retries until the element appears
        or the timeout is reached. No sleep() needed.
        """
        expect(self.page.locator(locator)).to_be_visible(timeout=self.timeout)

    @allure.step("Assert element contains text: {expected}")
    def assert_text(self, locator: str, expected: str):
        """
        Assert that an element contains specific text.
        Uses contains partial match is fine.
        'Submit Order' passes if element says 'Submit Order Now'.
        """
        expect(self.page.locator(locator)).to_contain_text(
            expected, timeout=self.timeout
        )

    @allure.step("Assert element is hidden: {locator}")
    def assert_hidden(self, locator: str):
        """
        Assert that an element is NOT visible.
        Used for negative tests error messages should
        not appear after a successful action.
        """
        expect(self.page.locator(locator)).to_be_hidden(timeout=self.timeout)

    @allure.step("Get text from element: {locator}")
    def get_text(self, locator: str) -> str:
        """
        Read the text content of an element and return it.
        Used when you need to verify a value that changes
        dynamically like an order number or a total price.
        """
        return self.page.locator(locator).inner_text()

    @allure.step("Wait for URL to contain: {url_part}")
    def wait_for_url(self, url_part: str):
        """
        Wait until the browser URL contains a specific string.
        Used after clicking buttons that trigger navigation.
        Safer than sleeping stops waiting as soon as URL matches.
        """
        self.page.wait_for_url(f"**{url_part}**", timeout=self.timeout)

    def take_screenshot(self, name: str = "screenshot"):
        """
        Manually take a screenshot and attach to Allure.
        Called explicitly when you want to capture a specific
        moment not just on failure.
        The conftest.py hook handles failure screenshots automatically.
        """
        allure.attach(
            self.page.screenshot(),
            name=name,
            attachment_type=allure.attachment_type.PNG,
        )
