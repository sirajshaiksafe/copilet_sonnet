# import asyncio
# import pytest
# from playwright.sync_api import Page
# from page_objects.base_page import BasePage
# from utils.api_client import API
# from utils.visual_comparison import VisualComparison
# from mocks.mock_server import MockServer
# from config.config import Config

# @pytest.fixture(scope="function")
# async def mock_server_instance():
#     """Setup mock API server"""
#     server = await MockServer.create(host=Config.MOCK_SERVER_HOST, port=Config.MOCK_SERVER_PORT)
#     # Mock basic page content
#     server.add_mock(
#         'GET',
#         '/',
#         {'html': '<h1>Example Domain</h1>'},
#         headers={'Content-Type': 'text/html'}
#     )

#     # Mock API endpoints
#     server.add_mock(
#         'GET',
#         '/api/users/1',
#         {'id': 1, 'name': 'Test User', 'email': 'test@example.com'}
#     )
#     yield server

#     # Clean up the server after test
#     await asyncio.sleep(0.1)  # Allow pending tasks to complete

# @pytest.mark.ui
# class TestSampleFeature:
#     @pytest.mark.asyncio
#     async def test_combined_capabilities(self, page_fixture: Page, mock_api: MockServer):
#         # Initialize components
#         base_page = BasePage(page_fixture)
#         api_client = API(base_url=Config.get_mock_server_url())
#         visual_comparison = VisualComparison(
#             baseline_dir=Config.BASELINE_DIR,
#             diff_dir=Config.DIFF_DIR
#         )

#         # Test UI interaction
#         base_page.navigate('/')
#         base_page.wait_for_element('h1')
#         assert base_page.get_text('h1') == 'Example Domain'

#         # Test API interaction
#         response = api_client.get('/api/users/1')
#         assert response.status_code == 200
#         user_data = response.json()
#         assert user_data['name'] == 'Test User'

#         # Test visual comparison
#         screenshot_path = base_page.take_screenshot('example_page')
#         is_match = visual_comparison.compare_screenshots(
#             screenshot_path,
#             'example_page.png'
#         )[0]  # Only get the is_match boolean, ignore diff_path
#         assert is_match, 'Visual difference detected'

#         # Verify mock API requests
#         requests = mock_api.get_requests()
#         assert len(requests) == 1
#         assert requests[0]['method'] == 'GET'
#         assert requests[0]['path'] == '/api/users/1'

#     @pytest.mark.benchmark
#     def test_performance(self, page_fixture: Page, benchmark):
#         base_page = BasePage(page_fixture)

#         def measure_load_time():
#             base_page.navigate('/')
#             base_page.wait_for_element('h1')

#         # Run performance benchmark
#         result = benchmark(measure_load_time)
#         metrics = {
#             'min': result.stats.get('min'),
#             'max': result.stats.get('max'),
#             'mean': result.stats.get('mean'),
#             'stddev': result.stats.get('stddev')
#         }

#         assert metrics['max'] < 5.0, 'Page load time exceeded 5 seconds'
