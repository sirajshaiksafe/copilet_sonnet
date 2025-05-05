import os
import json
import logging
import importlib
from typing import Dict, Any, Optional
from config.config import Config


class EnvironmentManager:
    """Utility for managing test environments and environment-specific data"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.env = Config.ENV
        self.logger.info(f"Environment initialized as: {self.env}")
        
        # Create directories for storing environment-specific data if they don't exist
        self._ensure_env_directories()
        
    def _ensure_env_directories(self) -> None:
        """Ensure directories for environment data exist"""
        env_dirs = [
            os.path.join("baseline_images", self.env.lower()),
            os.path.join("diff_images", self.env.lower()),
            os.path.join("test_data", self.env.lower()),
            os.path.join("reports", "screenshots", self.env.lower())
        ]
        
        for dir_path in env_dirs:
            if not os.path.exists(dir_path):
                os.makedirs(dir_path, exist_ok=True)
                self.logger.info(f"Created directory: {dir_path}")
    
    def get_base_url(self) -> str:
        """Get the base URL for the current environment"""
        return Config.get_environment_url()
    
    def get_current_env(self) -> str:
        """Get the current environment name"""
        return self.env
    
    def get_test_data(self, data_file: str) -> Dict[str, Any]:
        """Load environment-specific test data from JSON file"""
        env_data_path = os.path.join("test_data", self.env.lower(), data_file)
        default_data_path = os.path.join("test_data", "default", data_file)
        
        # Try environment-specific data first, then fall back to default
        data_path = env_data_path if os.path.exists(env_data_path) else default_data_path
        
        try:
            with open(data_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            self.logger.warning(f"Test data file not found: {data_path}")
            return {}
        except json.JSONDecodeError:
            self.logger.error(f"Invalid JSON in test data file: {data_path}")
            return {}
    
    def get_env_specific_value(self, key: str, default: Optional[Any] = None) -> Any:
        """Get an environment-specific value from environment variables"""
        env_specific_key = f"{self.env}_{key}"
        return os.getenv(env_specific_key, os.getenv(key, default))
    
    @staticmethod
    def set_environment(env: str) -> None:
        """Set the current environment"""
        os.environ['ENV'] = env.upper()
        # We need to reload config after changing environment
        import config.config
        importlib.reload(config.config)


# Create a singleton instance
env_manager = EnvironmentManager()