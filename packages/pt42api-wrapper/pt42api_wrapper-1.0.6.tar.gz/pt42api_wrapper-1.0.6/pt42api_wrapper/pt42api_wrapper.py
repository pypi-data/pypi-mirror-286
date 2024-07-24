"""Wrapper class for interacting with the PT42 API."""

import json
import requests
import sentry_sdk
import logging

from . import config
from .pt42api_token import ApiToken
from .utils import DateTimeEncoder


class ApiWrapper:
    """Wrapper class for interacting with the PT42 API."""

    def __init__(self, log_lvl=logging.INFO, *args, **kwargs):
        """Initializes the ApiWrapper class."""

        self._setup_logger(log_lvl)

        # Getting configuration from environment variables
        self.base_url = config.endpoint

        # Getting configuration from keyword arguments
        if 'base_url' in kwargs:
            self.base_url = kwargs['base_url']

        if 'sentry_dsn' in kwargs:
            self.sentry_dsn = kwargs.pop('sentry_dsn')
            self._setup_sentry()
        elif config.sentry:
            self.sentry_dsn = config.sentry
            self._setup_sentry()

        # Getting token and headers
        try:
            self.token = ApiToken(*args, **kwargs)
        except Exception as e:
            self.logger.error(e)

        self.headers = {
            'Authorization': f'Bearer {str(self.token)}',
            'Content-Type': 'application/json',
        }

    def req_handler(func):
        """Handles requests to the API."""

        def wrapper(
            self,
            method,
            url,
            data=None,
        ):
            # Refreshing the token if needed
            self.token.refresh_if_needed()
            self.headers = {
                'Authorization': f'Bearer {str(self.token)}',
                'Content-Type': 'application/json',
            }

            # Making the request
            endpoint = self.base_url + url
            try:
                json_dump = json.dumps(data)
            except (json.JSONDecodeError, TypeError):
                json_dump = json.dumps(data, cls=DateTimeEncoder)
            response = func(self, method, url=endpoint, data=json_dump)

            # Logging the response
            msg = f'{method} {url} "{response.status_code}" {response.reason}'
            try:
                response.raise_for_status()
                self.logger.debug(msg)
            except requests.exceptions.HTTPError:
                self.logger.error(msg)

            return response

        return wrapper

    @req_handler
    def request(self, method, url, data=None):
        """Requests to the API."""
        return requests.request(
            method,
            url=url,
            headers=self.headers,
            data=data,
        )

    def get(self, url, data={}):
        """GET request to the API."""
        return self.request(method='GET', url=url, data=data)

    def post(self, url, data):
        """POST request to the API."""
        return self.request(method='POST', url=url, data=data)

    def put(self, url, data):
        """PUT request to the API."""
        return self.request(method='PUT', url=url, data=data)

    def patch(self, url, data):
        """PATCH request to the API."""
        return self.request(method='PATCH', url=url, data=data)

    def delete(self, url):
        """DELETE request to the API."""
        return self.request(method='DELETE', url=url)

    def head(self, url):
        """HEAD request to the API."""
        return self.request(method='HEAD', url=url)

    def options(self, url):
        """OPTIONS request to the API."""
        return self.request(method='OPTIONS', url=url)

    def _setup_logger(self, log_lvl):
        """Sets up the logger."""

        # Setting up the logger
        self.logger = logging.getLogger('PT42API_Wrapper')
        self.logger.handlers.clear()
        self.logger.setLevel(log_lvl)

        # Creating a console handler
        handler = logging.StreamHandler()
        handler.setLevel(log_lvl)

        # Creating a formatter
        fmt = '%(name)s %(asctime)s - %(levelname)s: %(message)s'
        formatter = logging.Formatter(fmt)
        handler.setFormatter(formatter)

        # Adding the console handler to the logger
        self.logger.addHandler(handler)

    def _setup_sentry(self):
        """Setup a sentry connection"""
        sentry_sdk.init(
            dsn=self.sentry_dsn,
            traces_sample_rate=1.0,
            profiles_sample_rate=1.0,
        )
