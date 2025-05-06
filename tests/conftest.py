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
from utils.test_matrix import get_active_matrix


# Global flag to activate matrix testing automatically
AUTO_USE_MATRIX = True  # Set to True to always use the matrix


def pytest_addoption(parser):
    """Add command-line options for environment and browser selection"""
    parser.addoption(
        "--env", 
        action="store", 
        default="DEV", 
        help="Environment to run tests against: DEV, SYS, QA"
    )
    
    parser.addoption(
        "--browser-type", 
        action="store", 
        default="chromium", 
        help="Browser to use for UI tests: chromium, firefox, webkit"
    )
    
    parser.addoption(
        "--mobile-device", 
        action="store", 
        default="", 
        help=f"Mobile device to emulate: {', '.join(Config.get_supported_devices())}"
    )
    
    parser.addoption(
        "--matrix", 
        action="store_true", 
        default=AUTO_USE_MATRIX,  # Default to AUTO_USE_MATRIX setting
        help="Run tests on all active browser/device combinations defined in test matrix"
    )
    
    parser.addoption(
        "--skip-matrix", 
        action="store_true", 
        default=False,
        help="Skip matrix testing even if it's enabled by default"
    )


def pytest_configure(config):
    """Configure the test environment based on command line options"""
    # Handle matrix configuration
    use_matrix = config.getoption("--matrix")
    skip_matrix = config.getoption("--skip-matrix")
    
    if skip_matrix:
        # Force disable matrix if --skip-matrix is specified
        config.option.matrix = False
    
    # Set environment based on command line option
    env = config.getoption("--env").upper()
    if env not in ["DEV", "SYS", "QA"]:
        raise ValueError(f"Invalid environment: {env}. Must be one of: DEV, SYS, QA")
    
    env_manager.set_environment(env)
    
    # When not using matrix, set browser and device from command line
    if not config.getoption("--matrix"):
        # Set browser type
        browser_type = config.getoption("--browser-type").lower()
        if browser_type not in Config.get_supported_browsers():
            raise ValueError(f"Invalid browser type: {browser_type}. Must be one of: {', '.join(Config.get_supported_browsers())}")
        
        # Set device if specified
        device_name = config.getoption("--mobile-device")
        if device_name and device_name not in Config.get_supported_devices():
            raise ValueError(f"Invalid device name: {device_name}. Must be one of: {', '.join(Config.get_supported_devices())}")
        
        # Update environment variables
        os.environ["BROWSER_TYPE"] = browser_type
        os.environ["DEVICE_NAME"] = device_name
        
        # Print environment info for debugging
        print(f"\nRunning tests against {env} environment: {Config.get_environment_url()}")
        print(f"Browser: {browser_type}")
        if device_name:
            print(f"Device: {device_name}")
        print("\n")
    else:
        # Print matrix info
        matrix = get_active_matrix()
        print(f"\nRunning tests with matrix against {env} environment: {Config.get_environment_url()}")
        print(f"Active matrix ({len(matrix)} combinations):")
        for combo in matrix:
            print(f"  - {combo['name']}: Browser: {combo['browser_type']}, Device: {combo['mobile_device'] or 'Desktop'}")
        print("\n")


def pytest_generate_tests(metafunc):
    """
    Generate tests for each browser/device combination in the active matrix
    when matrix testing is enabled
    """
    # Apply matrix if it's active based on default or commandline
    if metafunc.config.getoption("--matrix"):
        # Get active matrix combinations
        active_matrix = get_active_matrix()
        
        # Parametrize all tests with browser_device_combo
        metafunc.parametrize(
            "browser_device_combo", 
            active_matrix,
            ids=[combo["name"] for combo in active_matrix],
            scope="function"
        )


@pytest.fixture(scope="function")
def browser_device_combo(request):
    """
    Default fixture for non-matrix test runs.
    When not using --matrix, this fixture provides a default combination
    """
    if not request.config.getoption("--matrix"):
        return {
            "name": "default",
            "browser_type": request.config.getoption("--browser-type"),
            "mobile_device": request.config.getoption("--mobile-device")
        }
    # For matrix runs, this fixture will be parametrized by pytest_generate_tests
    return request.param


@pytest.fixture(scope="function")
def browser(browser_device_combo) -> Generator[Browser, Any, None]:
    """Create a browser instance for the test."""
    # Set environment variables from the combo
    os.environ["BROWSER_TYPE"] = browser_device_combo["browser_type"]
    os.environ["DEVICE_NAME"] = browser_device_combo["mobile_device"]
    
    # Reload config to pick up the new environment variables
    import importlib
    from config import config
    importlib.reload(config)
    
    with sync_playwright() as playwright:
        if Config.BROWSER_TYPE == "chromium":
            created_browser = playwright.chromium.launch(**Config.get_browser_config())
        elif Config.BROWSER_TYPE == "firefox":
            created_browser = playwright.firefox.launch(**Config.get_browser_config())
        elif Config.BROWSER_TYPE == "webkit":
            created_browser = playwright.webkit.launch(**Config.get_browser_config())
        else:
            raise ValueError(f"Unsupported browser type: {Config.BROWSER_TYPE}")
            
        test_id = f"{browser_device_combo['name']} [{Config.BROWSER_TYPE}"
        if Config.DEVICE_NAME:
            test_id += f", {Config.DEVICE_NAME}"
        test_id += "]"
        print(f"\nStarting test with: {test_id}")
        
        yield created_browser
        created_browser.close()


@pytest.fixture
def context(browser: Browser) -> Generator[BrowserContext, Any, None]:
    """Create a browser context for each test with device emulation if specified."""
    # Get context options including device emulation settings
    context_options = Config.get_context_options()
    
    created_context = browser.new_context(**context_options)
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
