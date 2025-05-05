from page_objects.base_page import BasePage


class HomePage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.driver = page
        # Page locators
        self.file_a_claim_now_button = page.locator('#fileClaimId')
        self.navigation_menu = page.locator('nav.main-navigation')
        self.search_box = page.locator('#searchInput')
        self.search_button = page.locator('#searchButton')
        self.login_button = page.locator('#loginBtn')
        self.register_link = page.locator('#registerLink')
        self.hero_banner = page.locator('.hero-banner')
        self.featured_products = page.locator('.featured-product')
        self.footer_links = page.locator('footer .footer-links a')
        self.contact_us_link = page.locator('a[href*="contact"]')
        self.cookie_consent = page.locator('#cookieConsent')
        self.cookie_accept_button = page.locator('#acceptCookies')

    def navigate_to_home(self):
        """Navigate to the home page"""
        self.navigate(self.page.url)
        return self

    def click_file_claim_button(self):
        """Click on the 'File a Claim Now' button"""
        self.click('#fileClaimId')
        return self

    def search_for(self, query):
        """Perform a search using the search box"""
        self.fill(self.search_box, query)
        self.click(self.search_button)
        return self

    def click_login(self):
        """Click on the login button"""
        self.click(self.login_button)
        return self

    def click_register(self):
        """Click on the register link"""
        self.click(self.register_link)
        return self

    def get_featured_products_count(self):
        """Return the count of featured products"""
        return self.featured_products.count()

    def get_footer_links_count(self):
        """Return the count of footer links"""
        return self.footer_links.count()

    def accept_cookies(self):
        """Accept cookies if the consent banner is visible"""
        if self.is_element_visible(self.cookie_consent):
            self.click(self.cookie_accept_button)
        return self

    def verify_page_loaded(self):
        """Verify that the home page has loaded correctly"""
        return self.is_element_visible(self.hero_banner)

    def get_page_title(self):
        """Get the page title"""
        return self.page.title()
    
    def verify_navigation_menu_visible(self):
        """Verify that the navigation menu is visible"""
        return self.is_element_visible(self.navigation_menu)

    def click_contact_us(self):
        """Click on the Contact Us link"""
        self.click(self.contact_us_link)
        return self



