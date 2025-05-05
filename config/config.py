import os
from typing import Dict, Any, List

class Config:
    # Environment configuration
    ENV = os.getenv('ENV', 'SYS').upper()  # Default to SYS if not specified

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
    
    # Device configuration
    DEVICE_NAME = os.getenv('DEVICE_NAME', '')  # Empty string means no device emulation
    
    # Predefined device configurations
    DEVICES = {
        'pixel_5': {
            'user_agent': 'Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.104 Mobile Safari/537.36',
            'viewport': {'width': 393, 'height': 851},
            'device_scale_factor': 2.75,
            'is_mobile': True,
            'has_touch': True
        },
        'iphone_12': {
            'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1',
            'viewport': {'width': 390, 'height': 844},
            'device_scale_factor': 3,
            'is_mobile': True,
            'has_touch': True
        },
        'galaxy_tab_s7': {
            'user_agent': 'Mozilla/5.0 (Linux; Android 11; SM-T870) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.104 Safari/537.36',
            'viewport': {'width': 753, 'height': 1193},
            'device_scale_factor': 2,
            'is_mobile': True,
            'has_touch': True
        }
    }
    
    # Standard viewport for desktop testing
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
        
    @staticmethod
    def get_context_options() -> Dict[str, Any]:
        """Return context options including device emulation if specified"""
        options = {}
        
        # Set device emulation if specified
        if Config.DEVICE_NAME and Config.DEVICE_NAME in Config.DEVICES:
            options.update(Config.DEVICES[Config.DEVICE_NAME])
        else:
            options['viewport'] = Config.VIEWPORT
            
        # Add record video configuration if enabled
        if Config.VIDEO_RECORDING:
            options['record_video_dir'] = "reports/videos"
            
        return options

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

    @classmethod
    def get_supported_browsers(cls) -> List[str]:
        """Return list of supported browser types"""
        return ["chromium", "firefox", "webkit"]
        
    @classmethod
    def get_supported_devices(cls) -> List[str]:
        """Return list of supported mobile device emulations"""
        return list(cls.DEVICES.keys())
