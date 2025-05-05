import pytest
import allure
from playwright.sync_api import expect
from page_objects.home_page import HomePage
from config.config import Config


@allure.feature('Responsive Design')
class TestResponsiveDesign:
    
    @allure.title('Verify responsive design on mobile devices')
    @allure.severity(allure.severity_level.HIGH)
    @pytest.mark.parametrize("device_element", [
        ("#navigation_menu", False),  # (selector, expected_visibility)
        ("#mobile_menu_button", True),  # Mobile menu button should be visible
        (".hero-banner", True),  # Hero banner should be visible on mobile
    ])
    def test_responsive_elements_mobile(self, page, device_element):
        """
        Test that key elements behave correctly on mobile devices
        Skip if not running on a mobile device
        """
        # Skip if not running with a mobile device configuration
        if not Config.DEVICE_NAME:
            pytest.skip("This test requires a mobile device configuration")
            
        element_selector, should_be_visible = device_element
        
        # Initialize home page
        home_page = HomePage(page)
        
        # Accept cookies if present
        home_page.accept_cookies()
        
        # Verify element visibility based on expected behavior
        is_visible = page.locator(element_selector).is_visible()
        
        # Take screenshot for verification
        page.screenshot(path=f"reports/screenshots/responsive_{Config.DEVICE_NAME}_{element_selector.replace('#', '').replace('.', '')}.png")
        
        # Assert visibility is as expected
        assert is_visible == should_be_visible, f"Element {element_selector} visibility is {is_visible}, expected {should_be_visible}"
    
    @allure.title('Verify form functionality on mobile')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_mobile_form_interaction(self, page):
        """
        Test that forms can be properly interacted with on mobile devices
        """
        # Skip if not running with a mobile device configuration
        if not Config.DEVICE_NAME:
            pytest.skip("This test requires a mobile device configuration")
            
        # Initialize home page
        home_page = HomePage(page)
        
        # Accept cookies if present
        home_page.accept_cookies()
        
        # Click login button to go to login page
        if home_page.is_element_visible(home_page.login_button):
            home_page.click_login()
            
            # Verify we can interact with form fields in mobile view
            email_field = page.locator('input[type="email"]')
            password_field = page.locator('input[type="password"]')
            
            # Check if fields are visible and interactable
            assert email_field.is_visible(), "Email field not visible on mobile"
            assert password_field.is_visible(), "Password field not visible on mobile"
            
            # Test form interaction
            email_field.fill("test@example.com")
            password_field.fill("password123")
            
            # Take screenshot showing fields filled
            page.screenshot(path=f"reports/screenshots/mobile_form_{Config.DEVICE_NAME}.png")
            
            # Verify values were entered correctly
            assert email_field.input_value() == "test@example.com", "Email not entered correctly on mobile"
            assert password_field.input_value() == "password123", "Password not entered correctly on mobile"