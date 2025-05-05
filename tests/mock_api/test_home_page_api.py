import pytest
import allure
import json
from utils.api_client import ApiClient
from mocks.mock_server import setup_mock_endpoint


@allure.feature('Home Page API Tests')
class TestHomePageApi:
    
    @pytest.fixture
    def api_client(self):
        return ApiClient()
    
    @pytest.fixture
    def mock_home_data(self):
        """Setup mock data for home page API"""
        mock_data = {
            "heroSection": {
                "title": "Welcome to our Insurance Portal",
                "description": "Find the right coverage for your needs",
                "imageUrl": "hero-banner.jpg"
            },
            "featuredProducts": [
                {
                    "id": "auto-insurance",
                    "title": "Auto Insurance",
                    "description": "Comprehensive coverage for your vehicle",
                    "imageUrl": "auto-insurance.jpg"
                },
                {
                    "id": "home-insurance",
                    "title": "Home Insurance",
                    "description": "Protect your biggest investment",
                    "imageUrl": "home-insurance.jpg"
                },
                {
                    "id": "life-insurance",
                    "title": "Life Insurance",
                    "description": "Security for your family's future",
                    "imageUrl": "life-insurance.jpg"
                }
            ],
            "testimonials": [
                {
                    "name": "John Smith",
                    "comment": "Great service, saved me hundreds on my auto policy!",
                    "rating": 5
                },
                {
                    "name": "Sarah Johnson",
                    "comment": "Filing a claim was quick and easy.",
                    "rating": 4
                }
            ]
        }
        # Setup the mock endpoint
        setup_mock_endpoint('/api/home', 'GET', 200, mock_data)
        return mock_data

    @allure.title('Verify home page API returns correct data')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_home_page_api(self, api_client, mock_home_data):
        """
        Test that the home page API returns the expected data
        """
        # Make API request to the mock endpoint
        response = api_client.get('/api/home')
        
        # Verify response status code
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
        
        # Verify response data matches mock data
        response_data = response.json()
        assert response_data == mock_home_data, "API response data does not match expected mock data"

    @allure.title('Verify featured products API')
    @allure.severity(allure.severity_level.HIGH)
    def test_featured_products_api(self, api_client, mock_home_data):
        """
        Test that the featured products API returns correct products
        """
        # Setup mock endpoint for featured products
        featured_products = mock_home_data["featuredProducts"]
        setup_mock_endpoint('/api/products/featured', 'GET', 200, featured_products)
        
        # Make API request
        response = api_client.get('/api/products/featured')
        
        # Verify response status code
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
        
        # Verify response data
        response_data = response.json()
        assert len(response_data) == len(featured_products), f"Expected {len(featured_products)} products, got {len(response_data)}"
        
        # Verify product IDs
        product_ids = [product["id"] for product in response_data]
        expected_ids = [product["id"] for product in featured_products]
        assert set(product_ids) == set(expected_ids), f"Product IDs don't match. Expected: {expected_ids}, Got: {product_ids}"

    @allure.title('Verify API error handling')
    @allure.severity(allure.severity_level.NORMAL)
    def test_api_error_handling(self, api_client):
        """
        Test API error handling for non-existent endpoint
        """
        # Setup mock endpoint for 404 error
        error_response = {"error": "Not found", "code": 404}
        setup_mock_endpoint('/api/nonexistent', 'GET', 404, error_response)
        
        # Make API request to non-existent endpoint
        response = api_client.get('/api/nonexistent')
        
        # Verify response status code
        assert response.status_code == 404, f"Expected status code 404, got {response.status_code}"
        
        # Verify error response
        error_data = response.json()
        assert error_data["error"] == "Not found", f"Expected error message 'Not found', got '{error_data.get('error')}'"
        assert error_data["code"] == 404, f"Expected error code 404, got {error_data.get('code')}"