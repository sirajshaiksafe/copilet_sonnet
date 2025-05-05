"""
Test matrix configuration module for defining default test execution combinations
"""
from typing import Dict, List, Any
import os

# Define your default test matrix for browsers and devices
# This matrix determines which combinations will be run by default
DEFAULT_MATRIX = {
    # Format: 'name': {'browser_type': 'browser_name', 'mobile_device': 'device_name'}
    'chrome_desktop': {'browser_type': 'chromium', 'mobile_device': ''},
    'firefox_desktop': {'browser_type': 'firefox', 'mobile_device': ''},
    'chrome_pixel': {'browser_type': 'chromium', 'mobile_device': 'pixel_5'},
    'chrome_iphone': {'browser_type': 'chromium', 'mobile_device': 'iphone_12'},
    'chrome_tablet': {'browser_type': 'chromium', 'mobile_device': 'galaxy_tab_s7'},
}

# Active matrix - set which combinations from the DEFAULT_MATRIX should be active
# Just comment out any combinations you don't want to run
ACTIVE_COMBINATIONS = [
    'chrome_desktop',
    'chrome_pixel',
    # 'firefox_desktop',  # Commented out = not active
    # 'chrome_iphone',    # Commented out = not active
    # 'chrome_tablet',    # Commented out = not active
]

# Worker configuration
DEFAULT_WORKERS = int(os.getenv('DEFAULT_WORKERS', '2'))  # Default to 2 workers
MAX_WORKERS = int(os.getenv('MAX_WORKERS', '4'))  # Maximum 4 workers

def get_active_matrix() -> List[Dict[str, Any]]:
    """
    Return the active test matrix based on ACTIVE_COMBINATIONS
    """
    return [{'name': name, **DEFAULT_MATRIX[name]} for name in ACTIVE_COMBINATIONS if name in DEFAULT_MATRIX]

def get_recommended_workers() -> int:
    """
    Return the recommended number of workers based on active combinations
    """
    active_combos = len(get_active_matrix())
    # Use one worker per combination, but cap at MAX_WORKERS
    return min(max(active_combos, DEFAULT_WORKERS), MAX_WORKERS)

def get_matrix_command() -> str:
    """
    Return the pytest command to run the matrix with appropriate parallelism
    """
    workers = get_recommended_workers()
    return f"pytest --matrix -n{workers}"