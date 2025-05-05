# Modern Python Automation Framework with Playwright

This is a next-generation test automation framework built with Python and Playwright, incorporating AI-powered tools and comprehensive testing capabilities.

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
pip install playwright pytest pytest-playwright pytest-xdist pytest-html allure-pytest pytest-bdd requests pytest-mock pytest-timeout pytest-benchmark opencv-python pytest-check pytest-reportportal deepdiff aiohttp pytest-asyncio pytest-cov robotframework-requests pytest-metadata pymongo
```

4. Install Playwright browsers:
```bash
playwright install
```

## Framework Structure

```
automation-framework/
├── config/                 # Configuration files
├── tests/                  # Test files
│   ├── ui/                # UI tests
│   ├── api/               # API tests
│   └── visual/            # Visual tests
├── page_objects/          # Page Object Model files
├── utils/                 # Utility functions and helpers
├── data/                  # Test data
├── reports/               # Test reports
└── mocks/                 # API mocks
```

## Features

- **UI Testing**: Playwright-based UI automation
- **API Testing**: REST/GraphQL API testing capabilities
- **Visual Testing**: Screenshot comparison and visual regression
- **Mock API**: API mocking and stubbing
- **Performance**: Time tracking and benchmarking
- **Parallel Execution**: Multi-threaded test execution
- **Reporting**: 
  - HTML reports
  - Allure reports
  - ReportPortal integration
- **BDD Support**: Behavior Driven Development with pytest-bdd
- **Data Driven Testing**: Support for multiple data sources
- **CI/CD Integration**: Ready for continuous integration
- **AI Integration**: Support for AI-powered testing tools
- **Cross-browser Testing**: Support for multiple browsers
- **Screenshot & Video**: Automatic capture on failure
- **Logging**: Comprehensive logging system

## Running Tests

Basic test execution:
```bash
pytest
```

Run with parallel execution:
```bash
pytest -n auto
```

Generate HTML report:
```bash
pytest --html=reports/report.html
```

## Best Practices

- Use Page Object Model for UI tests
- Implement proper waiting strategies
- Use fixtures for setup and teardown
- Maintain test data separately
- Follow AAA (Arrange-Act-Assert) pattern
- Implement proper logging
- Use meaningful test names
- Keep tests independent
- Regular visual baseline updates

## Maintenance

- Regular updates of dependencies
- Periodic review of test cases
- Monitoring of test execution times
- Regular cleanup of test data
- Baseline image updates for visual testing

## Contributing

Please read CONTRIBUTING.md for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the LICENSE.md file for details