import sys
import os
site_packages = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'venv', 'Lib', 'site-packages')
if site_packages not in sys.path:
    sys.path.append(site_packages)

import pytest
from pytest_bdd import scenario, given, when, then, parsers
from playwright.sync_api import Page
from utils.api_client import APIClient
from config.config import Config
from dataclasses import dataclass
from typing import Optional

@dataclass
class APIResponseStore:
    """Store for API response data"""
    data: Optional[object] = None

@pytest.fixture
def response_store() -> APIResponseStore:
    """Fixture to store API response data per test"""
    return APIResponseStore()

# Scenarios
@scenario('../features/login.feature', 'Successful login with valid credentials')
def test_successful_login():
    """Test successful login with valid credentials"""
    # pytest-bdd manages this function

@scenario('../features/login.feature', 'Failed login attempts')
def test_failed_login():
    """Test failed login attempts"""
    # pytest-bdd manages this function

@scenario('../features/login.feature', 'Login API validation')
def test_api_login():
    """Test login API validation"""
    # pytest-bdd manages this function

# Background steps
@given('the application is running')
def check_application(page_fixture: Page):
    """Verify the application is running"""
    page_fixture.goto(Config.BASE_URL)
    assert page_fixture.url == Config.BASE_URL

@given('I am on the login page')
def navigate_to_login(page_fixture: Page):
    """Navigate to the login page"""
    page_fixture.goto(f"{Config.BASE_URL}/login")
    assert page_fixture.url.endswith('/login')

# UI steps
@when(parsers.parse('I enter "{value}" as {field_name}'))
def enter_field(page_fixture: Page, value: str, field_name: str):
    """Enter value in specified field"""
    selector = '#email' if field_name == 'email' else '#password'
    page_fixture.fill(selector, value)

@when('I click the login button')
def click_login(page_fixture: Page):
    """Click the login button"""
    page_fixture.click('#login-button')

@then('I should be redirected to the dashboard')
def verify_dashboard_redirect(page_fixture: Page):
    """Verify redirect to dashboard"""
    page_fixture.wait_for_url('**/dashboard')
    assert '/dashboard' in page_fixture.url

@then('I should see a welcome message with my name')
def verify_welcome_message(page_fixture: Page):
    """Verify welcome message is displayed"""
    welcome_text = page_fixture.text_content('.welcome-message')
    assert 'Welcome' in welcome_text

@then(parsers.parse('I should see an error message "{message}"'))
def verify_error_message(page_fixture: Page, message: str):
    """Verify error message is displayed"""
    error_text = page_fixture.text_content('.error-message')
    assert message in error_text

# API steps
@when('I send a POST request to "/api/login" with valid credentials')
def send_login_request(api_client: APIClient, api_response_store: APIResponseStore):
    """Send login API request"""
    response = api_client.post('/api/login', json_data={
        'email': 'valid@example.com',
        'password': 'validPassword123'
    })
    api_response_store.data = response

@then('the response status code should be 200')
def verify_status_code(api_response_store: APIResponseStore):
    """Verify API response status code"""
    assert api_response_store.data.status_code == 200

@then('the response should contain an authentication token')
def verify_auth_token(api_response_store: APIResponseStore):
    """Verify authentication token in response"""
    response_data = api_response_store.data.json()
    assert 'token' in response_data
    assert isinstance(response_data['token'], str)

@then('the response should contain the user profile')
def verify_user_profile(api_response_store: APIResponseStore):
    """Verify user profile in response"""
    response_data = api_response_store.data.json()
    assert 'user' in response_data
    user = response_data['user']
    assert 'id' in user
    assert 'email' in user
    assert 'name' in user