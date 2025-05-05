import os
from typing import Dict, Any

class Config:
    # Environment configuration
    ENV = os.getenv('ENV', 'SYS').upper()  # Default to QA if not specified

    # Environment URLs
    ENVIRONMENT_URLS = {
        'DEV': 'https://dev.safeliteforagents.com/',
        'SYS': 'https://sys.safeliteforagents.com/',
        'QA': 'https://qa.safeliteforagents.com/'
    }

    # Mock server configuration
    MOCK_SERVER_HOST = os.getenv('MOCK_SERVER_HOST', 'localhost')
    MOCK_SERVER_PORT = int(os.getenv('MOCK_SERVER_PORT', '8888'))
    BASELINE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "baseline_images", ENV.lower())
    DIFF_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "diff_images", ENV.lower())

    # Browser configuration
    BROWSER_TYPE = os.getenv('BROWSER_TYPE', 'chromium')  # chromium, firefox, or webkit
    HEADLESS = os.getenv('HEADLESS', 'True').lower() == 'true'
    SLOW_MO = int(os.getenv('SLOW_MO', '0'))
    VIEWPORT = {'width': 1920, 'height': 1080}

    # Test configuration
    BASE_URL = os.getenv('BASE_URL', ENVIRONMENT_URLS.get(ENV))
    TIMEOUT = int(os.getenv('TIMEOUT', '30000'))  # 30 seconds
    SCREENSHOT_ON_FAILURE = os.getenv('SCREENSHOT_ON_FAILURE', 'True').lower() == 'true'
    VIDEO_RECORDING = os.getenv('VIDEO_RECORDING', 'False').lower() == 'true'

    # API configuration
    API_BASE_URL = os.getenv('API_BASE_URL', BASE_URL)
    API_TIMEOUT = int(os.getenv('API_TIMEOUT', '10000'))  # 10 seconds

    # Report configuration
    REPORT_PORTAL = {
        'enabled': os.getenv('RP_ENABLED', 'False').lower() == 'true',
        'endpoint': os.getenv('RP_ENDPOINT', 'http://localhost:8080'),
        'project': os.getenv('RP_PROJECT', 'default_project'),
        'token': os.getenv('RP_TOKEN', ''),
    }

    @staticmethod
    def get_browser_config() -> Dict[str, Any]:
        """Return browser configuration for Playwright"""
        return {
            'headless': Config.HEADLESS,
            'slow_mo': Config.SLOW_MO
        }

    @classmethod
    def get_mock_server_url(cls) -> str:
        """Return the mock server URL"""
        return f'http://{cls.MOCK_SERVER_HOST}:{cls.MOCK_SERVER_PORT}'
    
    @classmethod
    def get_current_environment(cls) -> str:
        """Return the current environment name"""
        return cls.ENV
    
    @classmethod
    def get_environment_url(cls, env: str = None) -> str:
        """Return the URL for the specified environment or current environment if none specified"""
        env = env or cls.ENV
        return cls.ENVIRONMENT_URLS.get(env.upper())
