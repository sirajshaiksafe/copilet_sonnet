import os
import logging
from playwright.sync_api import Page
from config.config import Config
from typing import Any, Optional

class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.timeout = Config.TIMEOUT
        self.logger = logging.getLogger(__name__)

    def navigate(self, url: str) -> None:
        self.logger.info("Navigating to %s", url)
        self.page.goto(url)

    def wait_for_element(self, selector: str, timeout: Optional[int] = None) -> None:
        self.logger.info("Waiting for element %s", selector)
        self.page.wait_for_selector(selector, timeout=timeout or self.timeout)

    def click(self, selector: str) -> None:
        self.logger.info(f"Clicking element {selector}")
        self.page.click(selector)

    def fill(self, selector: str, value: str) -> None:
        self.logger.info(f"Filling {selector} with value")
        self.page.fill(selector, value)

    def get_text(self, selector: str) -> str:
        self.logger.info(f"Getting text from {selector}")
        return self.page.text_content(selector)

    def take_screenshot(self, name: str = "screenshot") -> str:
        """Take a screenshot and save it to the reports directory"""
        self.logger.info(f"Taking screenshot: {name}")
        path = f"reports/screenshots/{name}.png"
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self.page.screenshot(path=path)
        return path

    def is_element_visible(self, selector: str, timeout: Optional[int] = None) -> bool:
        self.logger.info(f"Checking if element exists: {selector}")
        try:
            self.page.wait_for_selector(selector, state="visible", 
                                      timeout=timeout or self.timeout)
            return True
        except:
            return False

    def get_attribute(self, selector: str, attr_name: str) -> Optional[str]:
        self.logger.info(f"Getting attribute {attr_name} from {selector}")
        element = self.page.locator(selector)
        return element.get_attribute(attr_name)

    def execute_script(self, script: str, *args: Any) -> Any:
        self.logger.info(f"Executing JavaScript")
        return self.page.evaluate(script, *args)