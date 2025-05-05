import pytest
import allure
from playwright.sync_api import expect
from page_objects.home_page import HomePage
from config.config import Config

@pytest.mark.ui
@allure.feature('Agent Login')
class TestSFA_Scenarios:
    
    @allure.title('Verify agent login functionality')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_agent_login(self, page):
        """Test agent login flow on SafeliteForAgents portal"""
        # Initialize the home page using our page object
        home_page = HomePage(page)
        
        # Navigate to the home page (using the environment URL from config)
        # The base URL is already set in the page fixture
        home_page.navigate(Config.BASE_URL)
        # Accept cookies if present
        home_page.accept_cookies()
        
        # Verify we're on the home page
        assert "Home" in page.title(), f"Unexpected page title: {page.title()}"
        
        # Take a screenshot for reporting
        home_page.take_screenshot("agent_login_home_page")
        
        # Further login steps would go here, like:
        # home_page.click_login()
        # login_page.enter_credentials("username", "password")
        # login_page.submit_login()
        # etc.