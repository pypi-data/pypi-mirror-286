import requests
from typing import Optional, Dict

class HttpRequestContext:
    """
    A base class for setting up a default request context for headers, params, etc.
    
    Args:
        base_url (str): The base URL for the API.
        default_headers (dict, optional): The default headers for the API. Defaults to None.
        default_params (dict, optional): The default parameters for the API. Defaults to None.
        
    Attributes:
        session (requests.Session): The requests Session instance.
    """
    
    def __init__(self, base_url: str, default_headers: Optional[Dict[str, str]] = None, default_params: Optional[Dict[str, str]] = None):
        self.session = requests.Session()
        self.session.headers.update(default_headers or {})
        self.session.params.update(default_params or {})
        self.base_url = base_url
        self.default_headers = default_headers
        self.default_params = default_params

    def get(self, endpoint: str, headers: Optional[Dict[str, str]] = None, params: Optional[Dict[str, str]] = None, **kwargs) -> requests.Response:
        return self.request('GET', endpoint, headers, params, **kwargs)

    def post(self, endpoint: str, headers: Optional[Dict[str, str]] = None, params: Optional[Dict[str, str]] = None, **kwargs) -> requests.Response:
        return self.request('POST', endpoint, headers, params, **kwargs)

    def put(self, endpoint: str, headers: Optional[Dict[str, str]] = None, params: Optional[Dict[str, str]] = None, **kwargs) -> requests.Response:
        return self.request('PUT', endpoint, headers, params, **kwargs)

    def delete(self, endpoint: str, headers: Optional[Dict[str, str]] = None, params: Optional[Dict[str, str]] = None, **kwargs) -> requests.Response:
        return self.request('DELETE', endpoint, headers, params, **kwargs)

    def request(self, method: str, endpoint: str, headers: Optional[Dict[str, str]] = None, params: Optional[Dict[str, str]] = None, **kwargs) -> requests.Response:
        """
        Makes an HTTP request.
        
        Args:
            method (str): The HTTP method.
            endpoint (str): The endpoint for the HTTP request.
            headers (dict, optional): The headers for the HTTP request. Defaults to None.
            params (dict, optional): The parameters for the HTTP request. Defaults to None.
            **kwargs: Additional arguments passed to requests.Session.request.
        
        Returns:
            The response from the HTTP request.
        """
        if headers:
            self.session.headers.update(headers)
        if params:
            self.session.params.update(params)
        
        response = self.session.request(method, self.base_url + endpoint, **kwargs)
        
        # Reset headers and params to defaults after each request
        self.session.headers = self.default_headers or {}
        self.session.params = self.default_params or {}
        
        return response
