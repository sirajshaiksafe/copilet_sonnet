import pytest
import allure
from playwright.sync_api import expect
from page_objects.home_page import HomePage


@allure.feature('Home Page')
class TestHomePage:

    @allure.title('Verify home page loads successfully')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_home_page_loads_successfully(self, page):
        """
        Test that the home page loads correctly with all main elements visible
        """
        home_page = HomePage(page)
        
        # Navigate to home page
        home_page.navigate(page.url)
        
        # Accept cookies if present
        home_page.accept_cookies()
        
        # Verify page loaded correctly
        assert home_page.verify_page_loaded(), "Home page did not load correctly"
        
        # Verify navigation menu is visible
        assert home_page.verify_navigation_menu_visible(), "Navigation menu is not visible"
        
        # Take screenshot for reporting
        home_page.take_screenshot("home_page_loaded")

    @allure.title('Verify search functionality')
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_functionality(self, page):
        """
        Test the search functionality on the home page
        """
        home_page = HomePage(page)
        search_query = "insurance"
        
        # Navigate to home page
        home_page.navigate(page.url)
        home_page.accept_cookies()
        
        # Perform search
        home_page.search_for(search_query)
        
        # Verify we've navigated to search results page
        # This would need to be customized based on your actual site behavior
        expect(page).to_have_url(f'*search*{search_query}*')
        
        # Take screenshot of search results
        home_page.take_screenshot("search_results")
    
    @allure.title('Verify login button redirects to login page')
    @allure.severity(allure.severity_level.HIGH)
    def test_login_button_redirection(self, page):
        """
        Test that clicking the login button redirects to the login page
        """
        home_page = HomePage(page)
        
        # Navigate to home page
        home_page.navigate(page.url)
        home_page.accept_cookies()
        
        # Click login button
        home_page.click_login()
        
        # Verify we've navigated to login page
        # This would need to be customized based on your actual site behavior
        expect(page).to_have_url('*login*')

    @allure.title('Verify register link redirects correctly')
    @allure.severity(allure.severity_level.HIGH)
    def test_register_link_redirection(self, page):
        """
        Test that clicking the register link redirects to the registration page
        """
        home_page = HomePage(page)
        
        # Navigate to home page
        home_page.navigate(page.url)
        home_page.accept_cookies()
        
        # Click register link
        home_page.click_register()
        
        # Verify we've navigated to register page
        # This would need to be customized based on your actual site behavior
        expect(page).to_have_url('*register*')

    @allure.title('Verify featured products are displayed')
    @allure.severity(allure.severity_level.NORMAL)
    def test_featured_products_displayed(self, page):
        """
        Test that featured products are displayed on the home page
        """
        home_page = HomePage(page)
        
        # Navigate to home page
        home_page.navigate(page.url)
        home_page.accept_cookies()
        
        # Verify featured products are displayed
        product_count = home_page.get_featured_products_count()
        assert product_count > 0, "No featured products are displayed"
        
        # Take screenshot
        home_page.take_screenshot("featured_products")

    @allure.title('Verify footer links')
    @allure.severity(allure.severity_level.MINOR)
    def test_footer_links(self, page):
        """
        Test that footer links are displayed
        """
        home_page = HomePage(page)
        
        # Navigate to home page
        home_page.navigate(page.url)
        home_page.accept_cookies()
        
        # Verify footer links are displayed
        links_count = home_page.get_footer_links_count()
        assert links_count > 0, "No footer links are displayed"

    @allure.title('Verify file claim button functionality')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_file_claim_button(self, page):
        """
        Test that file claim button works correctly
        """
        home_page = HomePage(page)
        
        # Navigate to home page
        home_page.navigate(page.url)
        home_page.accept_cookies()
        
        # Click file claim button
        home_page.click_file_claim_button()
        
        # Verify we've navigated to file claim page
        # This would need to be customized based on your actual site behavior
        expect(page).to_have_url('*claim*')

    @allure.title('Verify contact us link')
    @allure.severity(allure.severity_level.NORMAL)
    def test_contact_us_link(self, page):
        """
        Test that contact us link works correctly
        """
        home_page = HomePage(page)
        
        # Navigate to home page
        home_page.navigate(page.url)
        home_page.accept_cookies()
        
        # Click contact us link
        home_page.click_contact_us()
        
        # Verify we've navigated to contact page
        # This would need to be customized based on your actual site behavior
        expect(page).to_have_url('*contact*')

    @allure.title('Verify page title is correct')
    @allure.severity(allure.severity_level.MINOR)
    def test_page_title(self, page):
        """
        Test that the page title is correct
        """
        home_page = HomePage(page)
        
        # Navigate to home page
        home_page.navigate(page.url)
        
        # Verify page title
        title = home_page.get_page_title()
        assert "Home" in title, f"Page title '{title}' does not contain 'Home'"