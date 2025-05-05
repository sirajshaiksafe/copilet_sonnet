try:
    from aiohttp import web
except ImportError:
    import warnings
    warnings.warn("aiohttp is not installed properly, mock server functionality will be limited")
    raise

import json
from typing import Dict, Any, Optional, Union
import logging
import asyncio
from datetime import datetime

logger = logging.getLogger(__name__)

class MockServer:
    def __init__(self, host: str = 'localhost', port: int = 8000):
        self.host = host
        self.port = port
        self.app = web.Application()
        self.mocked_responses: Dict[str, Dict[str, Any]] = {}
        self.request_log: list = []
        self._setup_routes()
        
    def _setup_routes(self) -> None:
        """Set up the mock server routes"""
        self.app.router.add_route('*', '/{tail:.*}', self._handle_request)
        
    async def _handle_request(self, request: web.Request) -> web.Response:
        """Handle incoming requests and return mocked responses"""
        # Log request
        request_time = datetime.now()
        body = await request.text()
        request_data = {
            'method': request.method,
            'path': request.path,
            'headers': dict(request.headers),
            'query': dict(request.query),
            'body': body,
            'timestamp': request_time.isoformat()
        }
        self.request_log.append(request_data)
        
        # Find matching mock
        mock_key = f"{request.method}:{request.path}"
        if mock_key in self.mocked_responses:
            mock = self.mocked_responses[mock_key]
            await asyncio.sleep(mock.get('delay', 0))
            
            content_type = mock.get('headers', {}).get('Content-Type', 'application/json')
            body = mock.get('body', {})
            
            if 'html' in body and content_type == 'text/html':
                return web.Response(
                    status=mock.get('status', 200),
                    text=body['html'],
                    headers=mock.get('headers', {'Content-Type': 'text/html'})
                )
            elif content_type == 'application/json':
                return web.Response(
                    status=mock.get('status', 200),
                    body=json.dumps(body),
                    headers=mock.get('headers', {'Content-Type': 'application/json'})
                )
            else:
                return web.Response(
                    status=mock.get('status', 200),
                    body=str(body),
                    headers=mock.get('headers', {'Content-Type': 'text/plain'})
                )
            
        # No mock found
        logger.warning("No mock found for request: %s %s", request.method, request.path)
        return web.Response(
            status=404,
            body=json.dumps({'error': 'No mock found for this request'}),
            headers={'Content-Type': 'application/json'}
        )
        
    def add_mock(self, method: str, path: str, 
                response: Union[Dict[str, Any], str],
                status: int = 200, delay: float = 0,
                headers: Optional[Dict[str, str]] = None) -> None:
        """Add a mock response for a specific endpoint"""
        mock_key = f"{method}:{path}"
        
        # Auto-detect content type if not provided
        if headers is None:
            if isinstance(response, dict) and 'html' in response:
                headers = {'Content-Type': 'text/html'}
            elif isinstance(response, dict):
                headers = {'Content-Type': 'application/json'}
            else:
                headers = {'Content-Type': 'text/plain'}
                
        self.mocked_responses[mock_key] = {
            'body': response,
            'status': status,
            'delay': delay,
            'headers': headers
        }
        logger.info("Added mock for %s %s with content type %s", 
                   method, path, headers.get('Content-Type'))
        
    def clear_mocks(self) -> None:
        """Clear all mock responses"""
        self.mocked_responses.clear()
        logger.info("Cleared all mocks")
        
    def get_requests(self) -> list:
        """Get all recorded requests"""
        return self.request_log
        
    def clear_requests(self) -> None:
        """Clear request history"""
        self.request_log.clear()
        logger.info("Cleared request history")
        
    async def start(self) -> None:
        """Start the mock server"""
        runner = web.AppRunner(self.app)
        await runner.setup()
        site = web.TCPSite(runner, self.host, self.port)
        await site.start()
        logger.info("Mock server started at http://%s:%s", self.host, self.port)
        
    @classmethod
    async def create(cls, host: str = 'localhost', port: int = 8000) -> 'MockServer':
        """Create and start a mock server"""
        server = cls(host, port)
        await server.start()
        return server