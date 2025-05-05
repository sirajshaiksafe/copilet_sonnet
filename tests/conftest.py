import os
from datetime import datetime
from typing import Generator, Any
import asyncio
import warnings
from playwright.sync_api import Browser, BrowserContext, Page, sync_playwright
import pytest
from config.config import Config
from utils.api_client import API
from mocks.mock_server import MockServer
from utils.env_manager import env_manager


def pytest_addoption(parser):
    """Add command-line options for environment selection"""
    parser.addoption(
        "--env", 
        action="store", 
        default="DEV", 
        help="Environment to run tests against: DEV, SYS, QA"
    )


def pytest_configure(config):
    """Configure the test environment based on command line options"""
    # Set environment based on command line option
    env = config.getoption("--env").upper()
    if env not in ["DEV", "SYS", "QA"]:
        raise ValueError(f"Invalid environment: {env}. Must be one of: DEV, SYS, QA")
    
    env_manager.set_environment(env)
    
    # Print environment info for debugging
    print(f"\nRunning tests against {env} environment: {Config.get_environment_url()}\n")


@pytest.fixture(scope="session")
def browser() -> Generator[Browser, Any, None]:
    """Create a browser instance for the test session."""
    with sync_playwright() as playwright:
        if Config.BROWSER_TYPE == "chromium":
            created_browser = playwright.chromium.launch(**Config.get_browser_config())
        elif Config.BROWSER_TYPE == "firefox":
            created_browser = playwright.firefox.launch(**Config.get_browser_config())
        elif Config.BROWSER_TYPE == "webkit":
            created_browser = playwright.webkit.launch(**Config.get_browser_config())
        else:
            raise ValueError(f"Unsupported browser type: {Config.BROWSER_TYPE}")
        yield created_browser
        created_browser.close()

@pytest.fixture
def context(browser: Browser) -> Generator[BrowserContext, Any, None]:
    """Create a browser context for each test."""
    created_context = browser.new_context(
        viewport=Config.VIEWPORT,
        record_video_dir="reports/videos" if Config.VIDEO_RECORDING else None
    )
    yield created_context
    created_context.close()

@pytest.fixture
def page_fixture(context: BrowserContext) -> Generator[Page, Any, None]:
    """Create a new page for each test."""
    created_page = context.new_page()
    created_page.set_default_timeout(Config.TIMEOUT)
    yield created_page
    created_page.close()

@pytest.fixture(scope="session")
def base_url() -> str:
    """Return the base URL for the current environment"""
    return env_manager.get_base_url()

@pytest.fixture
def page(page_fixture, base_url) -> Page:
    """Configure page with environment-specific base URL"""
    # Set the base URL for navigation
    page_fixture.goto(base_url)
    return page_fixture

@pytest.fixture(scope="function")
async def mock_server_fixture():
    """Setup mock server with UI and API endpoints."""
    server = await MockServer.create(host=Config.MOCK_SERVER_HOST, port=Config.MOCK_SERVER_PORT)

    # Mock UI pages
    server.add_mock(
        'GET',
        '/',
        {
            'html': """
                <!DOCTYPE html>
                <html>
                <body>
                    <h1>Example Domain</h1>
                </body>
                </html>
            """
        },
        headers={'Content-Type': 'text/html'}
    )

    server.add_mock(
        'GET',
        '/login',
        {
            'html': """
                <!DOCTYPE html>
                <html>
                <body>
                    <form id="login-form">
                        <input type="email" id="email" name="email" />
                        <input type="password" id="password" name="password" />
                        <button id="login-button">Login</button>
                        <div class="error-message"></div>
                    </form>
                </body>
                </html>
            """
        },
        headers={'Content-Type': 'text/html'}
    )

    server.add_mock(
        'GET',
        '/dashboard',
        {
            'html': """
                <!DOCTYPE html>
                <html>
                <body>
                    <div class="welcome-message">Welcome Test User</div>
                </body>
                </html>
            """
        },
        headers={'Content-Type': 'text/html'}
    )

    # Mock API endpoints for successful login
    server.add_mock(
        'POST',
        '/api/login',
        {
            'token': 'mock-jwt-token',
            'user': {
                'id': 1,
                'email': 'valid@example.com',
                'name': 'Test User'
            }
        }
    )

    yield server
    # Clean up
    await asyncio.sleep(0.1)  # Allow pending tasks to complete

@pytest.fixture
def api_client() -> API:
    """Create an API client instance."""
    # Use environment-specific API URL
    api_base_url = env_manager.get_env_specific_value("API_BASE_URL", Config.API_BASE_URL)
    return API(base_url=api_base_url)

@pytest.fixture(autouse=True)
def test_context(request) -> Generator[None, Any, None]:
    """Provide test context information and handle failures."""
    # Setup test context
    test_name = request.node.name
    test_start_time = datetime.now()
    current_env = env_manager.get_current_env()

    yield

    # Handle test failure
    try:
        if hasattr(request.node, "rep_call") and request.node.rep_call.failed and Config.SCREENSHOT_ON_FAILURE:
            try:
                current_page = request.getfixturevalue('page_fixture')
                # Save screenshots in environment-specific directory
                screenshot_dir = f"reports/screenshots/{current_env.lower()}"
                os.makedirs(screenshot_dir, exist_ok=True)
                screenshot_path = f"{screenshot_dir}/{test_name}_{test_start_time:%Y%m%d_%H%M%S}.png"
                current_page.screenshot(path=screenshot_path)
            except (pytest.FixtureLookupError, IOError) as e:
                warnings.warn(f"Failed to capture screenshot: {str(e)}")
    except AttributeError:
        pass  # Node does not have rep_call attribute

@pytest.hookimpl(tryfirst=True)
def pytest_runtest_logreport(report):
    """Hook to store test results on test item for later use."""
    if report.when == "setup":
        # Only in setup phase, get the test item from the nodeid
        item = report.head_line  # Store the test name
        setattr(report, "test_name", item)  # Set an attribute on the report itself
