import os
from typing import Dict, Any

class Config:
    # Mock server configuration
    MOCK_SERVER_HOST = os.getenv('MOCK_SERVER_HOST', 'localhost')
    MOCK_SERVER_PORT = int(os.getenv('MOCK_SERVER_PORT', '8888'))
    
    # Browser configuration
    BROWSER_TYPE = os.getenv('BROWSER_TYPE', 'chromium')  # chromium, firefox, or webkit
    HEADLESS = os.getenv('HEADLESS', 'True').lower() == 'true'
    SLOW_MO = int(os.getenv('SLOW_MO', '0'))
    VIEWPORT = {'width': 1920, 'height': 1080}
    
    # Test configuration
    BASE_URL = os.getenv('BASE_URL', f'http://{MOCK_SERVER_HOST}:{MOCK_SERVER_PORT}')
    TIMEOUT = int(os.getenv('TIMEOUT', '30000'))  # 30 seconds
    SCREENSHOT_ON_FAILURE = os.getenv('SCREENSHOT_ON_FAILURE', 'True').lower() == 'true'
    VIDEO_RECORDING = os.getenv('VIDEO_RECORDING', 'False').lower() == 'true'
    
    # API configuration
    API_BASE_URL = os.getenv('API_BASE_URL', f'http://{MOCK_SERVER_HOST}:{MOCK_SERVER_PORT}')
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