import pytest
import allure
import json
from playwright.sync_api import expect
from page_objects.home_page import HomePage


@allure.feature('Home Page Accessibility Tests')
class TestHomePageAccessibility:

    @pytest.fixture
    def run_axe(self, page):
        """Run axe accessibility analysis on the page"""
        # Helper function to inject and run axe-core
        def _run_axe():
            # Inject axe-core library (typically loaded from CDN in real implementation)
            page.add_script_tag(url="https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.5.2/axe.min.js")
            
            # Run axe analysis
            results = page.evaluate("""
                () => {
                    return new Promise(resolve => {
                        axe.run(document, { resultTypes: ['violations'] }, (err, results) => {
                            resolve(results);
                        });
                    });
                }
            """)
            return results
        return _run_axe
    
    @allure.title('Verify home page meets WCAG 2.1 AA compliance')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_home_page_accessibility(self, page, run_axe):
        """
        Test that the home page meets WCAG 2.1 AA accessibility standards
        """
        home_page = HomePage(page)
        
        # Navigate to home page
        home_page.navigate(page.url)
        home_page.accept_cookies()
        
        # Run accessibility analysis
        results = run_axe()
        
        # Log violations for reporting
        violations = results.get('violations', [])
        for violation in violations:
            allure.attach(
                json.dumps(violation, indent=2),
                f"Accessibility violation: {violation.get('id')}",
                allure.attachment_type.JSON
            )
        
        # Assert no critical or serious violations
        critical_violations = [v for v in violations if v.get('impact') in ['critical', 'serious']]
        assert len(critical_violations) == 0, f"Found {len(critical_violations)} critical/serious accessibility violations"

    @allure.title('Verify keyboard navigation')
    @allure.severity(allure.severity_level.HIGH)
    def test_keyboard_navigation(self, page):
        """
        Test that the home page is fully navigable using keyboard
        """
        home_page = HomePage(page)
        
        # Navigate to home page
        home_page.navigate(page.url)
        home_page.accept_cookies()
        
        # Simulate keyboard navigation through major page elements
        # Press Tab key multiple times to navigate through focusable elements
        page.keyboard.press('Tab')  # First focusable element
        
        # Get the currently focused element
        focused_element = page.evaluate("() => document.activeElement.tagName")
        assert focused_element is not None, "No element is focused after Tab press"
        
        # Continue tabbing and verify we can reach major interactive elements
        interactive_elements = ['a', 'button', 'input', 'select', 'textarea']
        found_elements = set()
        
        # Simulate tabbing through 10 elements (adjust based on your page)
        for _ in range(10):
            element_tag = page.evaluate("() => document.activeElement.tagName.toLowerCase()")
            if element_tag in interactive_elements:
                found_elements.add(element_tag)
            page.keyboard.press('Tab')
        
        # Assert we found at least some interactive elements
        assert len(found_elements) > 0, "Could not navigate to any interactive elements using keyboard"
        
    @allure.title('Verify screen reader accessibility')
    @allure.severity(allure.severity_level.HIGH)
    def test_screen_reader_accessibility(self, page):
        """
        Test that the home page has proper ARIA attributes and alt text
        """
        home_page = HomePage(page)
        
        # Navigate to home page
        home_page.navigate(page.url)
        home_page.accept_cookies()
        
        # Check for alt text on all images
        missing_alt = page.evaluate("""
            () => {
                const images = Array.from(document.querySelectorAll('img'));
                return images.filter(img => !img.hasAttribute('alt')).length;
            }
        """)
        assert missing_alt == 0, f"Found {missing_alt} images without alt text"
        
        # Check that buttons have accessible names
        buttons_without_name = page.evaluate("""
            () => {
                const buttons = Array.from(document.querySelectorAll('button, [role="button"]'));
                return buttons.filter(button => !button.textContent.trim() && !button.hasAttribute('aria-label') && !button.hasAttribute('title')).length;
            }
        """)
        assert buttons_without_name == 0, f"Found {buttons_without_name} buttons without accessible names"
        
        # Check for proper heading structure
        improper_headings = page.evaluate("""
            () => {
                const headings = Array.from(document.querySelectorAll('h1, h2, h3, h4, h5, h6'));
                let prevLevel = 0;
                let improperCount = 0;
                
                for (const heading of headings) {
                    const level = parseInt(heading.tagName[1]);
                    if (prevLevel > 0 && level > prevLevel + 1) {
                        improperCount++;
                    }
                    prevLevel = level;
                }
                
                return improperCount;
            }
        """)
        assert improper_headings == 0, f"Found {improper_headings} improper heading level jumps"

    @allure.title('Verify color contrast compliance')
    @allure.severity(allure.severity_level.NORMAL)
    def test_color_contrast(self, page, run_axe):
        """
        Test that the home page has sufficient color contrast for text elements
        """
        home_page = HomePage(page)
        
        # Navigate to home page
        home_page.navigate(page.url)
        home_page.accept_cookies()
        
        # Run accessibility analysis
        results = run_axe()
        
        # Filter for color contrast violations
        contrast_violations = [v for v in results.get('violations', []) if 'color-contrast' in v.get('id', '')]
        
        # Log contrast violations for reporting
        for violation in contrast_violations:
            allure.attach(
                json.dumps(violation, indent=2),
                f"Color contrast violation: {violation.get('id')}",
                allure.attachment_type.JSON
            )
        
        # Assert no color contrast violations
        assert len(contrast_violations) == 0, f"Found {len(contrast_violations)} color contrast violations"