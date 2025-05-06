# Hybrid Playwright Test Automation Framework for SafeliteForAgents

A comprehensive, multi-environment testing framework built with Python and Playwright, providing UI, Visual, API, and Accessibility testing capabilities.

## Table of Contents
- [Framework Overview](#framework-overview)
- [Setup Instructions](#setup-instructions)
- [Framework Structure](#framework-structure)
- [Environment Management](#environment-management)
- [Test Matrix Configuration](#test-matrix-configuration)
- [Parallel Execution](#parallel-execution)
- [Running Tests](#running-tests)
- [Test Types](#test-types)
- [Mobile and Multi-Browser Testing](#mobile-and-multi-browser-testing)
- [Visual Testing](#visual-testing)
- [API Mock Testing](#api-mock-testing)
- [Accessibility Testing](#accessibility-testing)
- [Reporting](#reporting)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

## Framework Overview

This framework enables comprehensive testing of the SafeliteForAgents web application across multiple environments (DEV, SYS, QA), browsers, and device types. It supports:

- Multi-environment testing (DEV, SYS, QA)
- Cross-browser testing (Chrome, Firefox, Safari)
- Mobile device emulation
- Visual regression testing
- Mock API testing
- Accessibility testing
- Parallel test execution

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- VS Code with Python extensions

### Environment Setup

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
- Windows:
```bash
.\venv\Scripts\activate
```
- Linux/Mac:
```bash
source venv/bin/activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Install Playwright browsers:
```bash
playwright install
```

## Framework Structure

```
hybrid_framework_SFA/
├── .gitignore                # Git ignore file
├── README.md                 # This documentation
├── pytest.ini                # Pytest configuration
├── pyproject.toml            # Project metadata
├── requirements.txt          # Dependencies
├── run_matrix.py             # Script for matrix execution
├── config/                   # Configuration files
│   └── config.py             # Central configuration
├── tests/                    # Test files organized by type
│   ├── conftest.py           # Test fixtures and setup
│   ├── ui/                   # UI functional tests
│   ├── visual/               # Visual testing
│   ├── mock_api/             # API mock testing
│   └── accessibility/        # Accessibility testing
├── page_objects/             # Page Object Model files
│   ├── base_page.py          # Base page class
│   └── home_page.py          # Home page implementation
├── utils/                    # Utilities and helpers
│   ├── api_client.py         # API client utility
│   ├── env_manager.py        # Environment manager
│   ├── test_matrix.py        # Test matrix configuration
│   └── visual_comparison.py  # Visual comparison utility
├── mocks/                    # API mocking utilities
│   └── mock_server.py        # Mock server implementation
├── baseline_images/          # Visual testing baselines by env
│   ├── dev/
│   ├── sys/
│   └── qa/
├── diff_images/              # Visual testing differences by env
├── test_data/                # Test data by environment
└── reports/                  # Test reports and results
    ├── screenshots/          # Failure screenshots
    └── videos/               # Test recordings
```

## Environment Management

The framework supports three environments: DEV, SYS, and QA.

### Environment URLs:
- DEV: https://dev.safeliteforagents.com/
- SYS: https://sys.safeliteforagents.com/
- QA: https://qa.safeliteforagents.com/

### How to Change Default Environment

1. Edit `config/config.py`:
```python
# Change the default environment here
ENV = os.getenv('ENV', 'SYS').upper()  # Options: DEV, SYS, QA
```

2. Or specify when running tests:
```bash
pytest --env=QA tests/ui/test_home_page.py
```

### Environment-Specific Artifacts

The framework automatically maintains separate directories for each environment:
- Test data: `test_data/{env}/`
- Baseline images: `baseline_images/{env}/`
- Difference images: `diff_images/{env}/`
- Screenshots: `reports/screenshots/{env}/`

## Test Matrix Configuration

The test matrix defines which browser and device combinations to test on. Configure this in `utils/test_matrix.py`:

```python
# Define which browser/device combinations are active
ACTIVE_COMBINATIONS = [
    'chrome_desktop',
    'chrome_pixel',
    # 'firefox_desktop',  # Commented out = not active
    # 'chrome_iphone',    # Commented out = not active
    # 'chrome_tablet',    # Commented out = not active
]
```

### Adding New Devices

Add new device configurations in `config/config.py` under the `DEVICES` dictionary:

```python
DEVICES = {
    # Existing devices
    # ...
    'new_device_name': {
        'user_agent': 'User-Agent-String',
        'viewport': {'width': 1024, 'height': 768},
        'device_scale_factor': 2,
        'is_mobile': True,
        'has_touch': True
    }
}
```

## Parallel Execution

The framework automatically runs tests in parallel. Configure workers in `pytest.ini`:

```ini
# Default to 2 workers
addopts = -v --html=reports/report.html --self-contained-html -n2
```

Or specify workers when running:
```bash
pytest -n4 tests/ui/  # Run with 4 workers
```

## Running Tests

### Standard Test Run (Uses Matrix Automatically)
```bash
# Run UI tests with default matrix and parallelism
pytest tests/ui/test_home_page.py

# Run on specific environment
pytest tests/ui/test_home_page.py --env=QA

# Skip matrix (single browser/device)
pytest tests/ui/test_home_page.py --skip-matrix
```

### Browser-Specific Tests
```bash
# Run tests on Firefox (bypassing matrix)
pytest tests/ui/test_home_page.py --skip-matrix --browser-type=firefox
```

### Device-Specific Tests
```bash
# Run tests on Pixel 5 (bypassing matrix)
pytest tests/ui/test_home_page.py --skip-matrix --mobile-device=pixel_5
```

## Test Types

The framework supports different types of tests, organized in separate directories:

### UI Testing
Standard UI functional tests that verify application behavior:
```bash
pytest tests/ui/
```

### Visual Testing
Visual regression tests that compare screenshots against baselines:
```bash
pytest tests/visual/
```

### API Mock Testing
Tests that use mock API responses to verify frontend behavior:
```bash
pytest tests/mock_api/
```

### Accessibility Testing
Tests that verify WCAG compliance and accessibility standards:
```bash
pytest tests/accessibility/
```

## Mobile and Multi-Browser Testing

The framework supports testing on multiple browsers and mobile device emulations.

### Available Browsers
- chromium (default)
- firefox
- webkit (Safari)

### Configured Mobile Devices
- pixel_5 (Android phone)
- iphone_12 (iOS phone)
- galaxy_tab_s7 (Android tablet)

## Visual Testing

Visual testing compares screenshots against baseline images to detect visual regressions.

### Creating Baselines
First run with `--update-baseline` to create baseline images:
```bash
pytest tests/visual/ --update-baseline
```

### Running Visual Tests
Then run visual tests normally:
```bash
pytest tests/visual/
```

### Visual Test Reports
Check diff images in `diff_images/{env}/` when visual tests fail.

## API Mock Testing

API mock testing uses a mock server to simulate backend responses.

### Configure Mock Responses
Define mock responses in `mocks/mock_server.py` or in test fixtures.

### Running API Mock Tests
```bash
pytest tests/mock_api/
```

## Accessibility Testing

Accessibility tests verify compliance with WCAG guidelines.

### Running Accessibility Tests
```bash
pytest tests/accessibility/
```

## Reporting

The framework generates multiple report formats:

### HTML Reports
Generated after each run at `reports/report.html`.

### Allure Reports
Generate and view with:
```bash
pytest --alluredir=./reports/allure-results
allure serve ./reports/allure-results
```

### Screenshots and Videos
- Failure screenshots: `reports/screenshots/{env}/`
- Test videos (when enabled): `reports/videos/`

## Best Practices

- Use Page Object Model for UI interactions
- Keep test data separate from test logic
- Use environment-specific test data
- Update visual baselines when intended UI changes occur
- Run tests across all environments before releases
- Use descriptive test names with the pattern `test_should_*`
- Include proper test documentation with docstrings

## Troubleshooting

### Parameter Conflicts
If you encounter parameter conflicts like:
```
argparse.ArgumentError: argument --browser: conflicting option string: --browser
```
Use custom parameter names in `conftest.py` like `--browser-type` instead of `--browser`.

### Scope Mismatch
For scope mismatch errors, ensure fixture scopes are compatible:
```python
@pytest.fixture(scope="session")  # Match the required scope
def base_url():
    # ...
```

### SyntaxError
If you see unexpected syntax errors, check Python version compatibility and that all files are properly formatted.

### Browser/Device Not Working
Check that the device configuration in `config.py` is correct and that you've installed the required browser with `playwright install`.