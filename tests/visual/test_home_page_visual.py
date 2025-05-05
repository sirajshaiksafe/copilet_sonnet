import pytest
import allure
from playwright.sync_api import expect
from page_objects.home_page import HomePage
from config.config import Config
from utils.visual_comparison import VisualComparison


@allure.feature('Home Page Visual Tests')
class TestHomePageVisual:
    
    @pytest.fixture
    def visual_comparison(self):
        return VisualComparison(Config.BASELINE_DIR, Config.DIFF_DIR)

    @allure.title('Verify home page responsive design - mobile')
    @allure.severity(allure.severity_level.NORMAL)
    def test_home_page_responsive_mobile(self, page, visual_comparison):
        """
        Test that the home page displays correctly on mobile devices
        """
        # Set viewport to mobile size
        page.set_viewport_size({"width": 375, "height": 812})  # iPhone X dimensions
        
        home_page = HomePage(page)
        
        # Navigate to home page
        home_page.navigate(page.url)
        home_page.accept_cookies()
        
        # Take screenshot for visual comparison
        screenshot_path = home_page.take_screenshot("home_page_mobile_view")
        
        # Capture screenshot and verify with visual comparison tool
        screenshot_bytes = page.screenshot()
        match_result, message = visual_comparison.compare_screenshots(
            screenshot_bytes, "home_page_mobile_view"
        )
        
        # Assert the visual comparison
        assert match_result, message
        
        # Verify key elements are still visible on mobile
        assert home_page.verify_page_loaded(), "Home page did not load correctly on mobile"

    @allure.title('Verify home page responsive design - tablet')
    @allure.severity(allure.severity_level.NORMAL)
    def test_home_page_responsive_tablet(self, page, visual_comparison):
        """
        Test that the home page displays correctly on tablet devices
        """
        # Set viewport to tablet size
        page.set_viewport_size({"width": 768, "height": 1024})  # iPad dimensions
        
        home_page = HomePage(page)
        
        # Navigate to home page
        home_page.navigate(page.url)
        home_page.accept_cookies()
        
        # Capture screenshot and verify with visual comparison tool
        screenshot_bytes = page.screenshot()
        match_result, message = visual_comparison.compare_screenshots(
            screenshot_bytes, "home_page_tablet_view"
        )
        
        # Assert the visual comparison
        assert match_result, message
        
        # Verify key elements are still visible on tablet
        assert home_page.verify_page_loaded(), "Home page did not load correctly on tablet"

    @allure.title('Verify home page visual regression')
    @allure.severity(allure.severity_level.NORMAL)
    def test_home_page_visual_regression(self, page, visual_comparison):
        """
        Test for visual regression on the home page
        """
        home_page = HomePage(page)
        
        # Navigate to home page
        home_page.navigate(page.url)
        home_page.accept_cookies()
        
        # Capture screenshot and verify with visual comparison tool
        screenshot_bytes = page.screenshot()
        match_result, message = visual_comparison.compare_screenshots(
            screenshot_bytes, "home_page_visual"
        )
        
        # Assert the visual comparison
        assert match_result, message
    
    @allure.title('Verify dark mode support')
    @allure.severity(allure.severity_level.MINOR)
    def test_home_page_dark_mode(self, page, visual_comparison):
        """
        Test that the home page supports dark mode (if applicable)
        """
        # Force dark mode via CSS media query emulation
        page.emulate_media(color_scheme="dark")
        
        home_page = HomePage(page)
        
        # Navigate to home page
        home_page.navigate(page.url)
        home_page.accept_cookies()
        
        # Capture screenshot and verify with visual comparison tool
        screenshot_bytes = page.screenshot()
        match_result, message = visual_comparison.compare_screenshots(
            screenshot_bytes, "home_page_dark_mode"
        )
        
        # Assert the visual comparison
        assert match_result, message
        
        # Verify page loaded correctly in dark mode
        assert home_page.verify_page_loaded(), "Home page did not load correctly in dark mode"

    @allure.title('Verify critical element visual appearance')
    @allure.severity(allure.severity_level.HIGH)
    def test_critical_elements_visual(self, page, visual_comparison):
        """
        Test the visual appearance of critical elements like buttons and forms
        """
        home_page = HomePage(page)
        
        # Navigate to home page
        home_page.navigate(page.url)
        home_page.accept_cookies()
        
        # Take screenshots of critical elements
        # Example: Screenshot of login button
        login_button = page.locator(home_page.login_button)
        login_button_screenshot = login_button.screenshot()
        
        # Compare with baseline
        match_result, message = visual_comparison.compare_screenshots(
            login_button_screenshot, "login_button"
        )
        
        # Assert the visual comparison
        assert match_result, message
        
        # Example: Screenshot of file claim button
        claim_button = page.locator(home_page.file_a_claim_now_button)
        claim_button_screenshot = claim_button.screenshot()
        
        # Compare with baseline
        match_result, message = visual_comparison.compare_screenshots(
            claim_button_screenshot, "file_claim_button"
        )
        
        # Assert the visual comparison
        assert match_result, message