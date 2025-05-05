import json
import logging
import requests
from typing import Any, Dict, Optional
from config.config import Config

logger = logging.getLogger(__name__)

class API:
    def __init__(self, base_url: Optional[str] = None):
        self.base_url = base_url or Config.API_BASE_URL
        self.session = requests.Session()
        self.timeout = Config.API_TIMEOUT / 1000  # Convert to seconds

    def _log_request_response(self, response: requests.Response, data: Optional[Dict[str, Any]] = None) -> None:
        """Log request and response details"""
        logger.info(f"Request URL: {response.request.url}")
        logger.info(f"Request Method: {response.request.method}")
        
        if data:
            logger.info(f"Request Data: {json.dumps(data, indent=2)}")
            
        try:
            response_json = response.json()
            logger.info(f"Response: {json.dumps(response_json, indent=2)}")
        except json.JSONDecodeError:
            logger.info(f"Response Text: {response.text}")

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None, **kwargs: Any) -> requests.Response:
        response = self.session.get(f"{self.base_url}/{endpoint.lstrip('/')}", params=params, timeout=self.timeout, **kwargs)
        self._log_request_response(response)
        return response

    def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None, json_data: Optional[Dict[str, Any]] = None, **kwargs: Any) -> requests.Response:
        response = self.session.post(f"{self.base_url}/{endpoint.lstrip('/')}", json=json_data, data=data, timeout=self.timeout, **kwargs)
        self._log_request_response(response, json_data or data)
        return response

    def put(self, endpoint: str, data: Optional[Dict[str, Any]] = None, json_data: Optional[Dict[str, Any]] = None, **kwargs: Any) -> requests.Response:
        response = self.session.put(f"{self.base_url}/{endpoint.lstrip('/')}", json=json_data, data=data, timeout=self.timeout, **kwargs)
        self._log_request_response(response, json_data or data)
        return response

    def delete(self, endpoint: str, **kwargs: Any) -> requests.Response:
        response = self.session.delete(f"{self.base_url}/{endpoint.lstrip('/')}", timeout=self.timeout, **kwargs)
        self._log_request_response(response)
        return response

    def patch(self, endpoint: str, data: Optional[Dict[str, Any]] = None, json_data: Optional[Dict[str, Any]] = None, **kwargs: Any) -> requests.Response:
        response = self.session.patch(f"{self.base_url}/{endpoint.lstrip('/')}", json=json_data, data=data, timeout=self.timeout, **kwargs)
        self._log_request_response(response, json_data or data)
        return response

    def set_headers(self, headers: Dict[str, str]) -> None:
        """Set default headers for all requests"""
        self.session.headers.update(headers)

    def set_token(self, token: str) -> None:
        """Set bearer token for authentication"""
        self.session.headers['Authorization'] = f'Bearer {token}'