"""This module provides a class to represent a valid token from the auth
provider. Used to authenticate requests to the API.
"""

import time
import requests

from . import config


class ApiToken:
    """Represents a valid token from the auth provider.
    Used to authenticate requests to the API.
    """

    json = None

    def __init__(self, *args, **kwargs):
        """Initializes the ApiToken class."""

        # Getting configuration from environment variables
        self.auth_url = config.auth_url
        self.credentials = config.credentials.copy()

        # Overriding configuration with keyword arguments
        if 'auth_url' in kwargs:
            self.auth_url = kwargs['auth_url']
        if 'client_id' in kwargs:
            self.credentials['client_id'] = kwargs['client_id']
        if 'client_secret' in kwargs:
            self.credentials['client_secret'] = kwargs['client_secret']
        if 'grant_type' in kwargs:
            self.credentials['grant_type'] = kwargs['grant_type']
        if 'scope' in kwargs:
            self.credentials['scope'] = kwargs['scope']

        # Checking if all required configurations are present
        assert (
            self.auth_url
        ), "missing 1 required keyword-only argument: 'auth_url'"
        assert self.credentials[
            'client_id'
        ], "missing 1 required keyword-only argument: 'client_id'"
        assert self.credentials[
            'client_secret'
        ], "missing 1 required keyword-only argument: 'client_secret'"
        assert self.credentials[
            'grant_type'
        ], "missing 1 required keyword-only argument: 'grant_type'"

        # Fetching token from auth provider
        self.get()

    def get(self):
        """Fetches a token from the auth provider."""

        url = self.auth_url + '/token'

        response = requests.post(url=url, data=self.credentials)
        response.raise_for_status()

        self.json = response.json()

        return self.json

    def refresh_if_needed(self):
        """Refreshes the token if it needs to be refreshed."""

        if self.needs_refresh():
            self.refresh()

    def needs_refresh(self):
        """Checks if the token needs to be refreshed."""

        info = self.info()
        return 'active' not in info or not info['active']

    def refresh(self):
        """Refreshes the token."""

        assert (
            self.json
        ), f'{self.__class__.__name__} needs to call get() method'

        url = self.auth_url + '/token'
        credentials = self.credentials.copy()
        credentials['grant_type'] = 'refresh_token'
        credentials['refresh_token'] = self.json['refresh_token']

        response = requests.post(url=url, data=credentials)
        response.raise_for_status()

        self.fetched_at = int(time.time())
        self.json = response.json()
        return self.json

    def revoke(self):
        """Revokes the token."""

        assert self.json, (
            '%s needs to call get() method first' % self.__class__.__name__
        )

        url = self.auth_url + '/logout'
        credentials = self.credentials.copy()
        credentials['grant_type'] = 'refresh_token'
        headers = {'Authorization': 'Bearer ' + str(self)}

        response = requests.post(url=url, data=credentials, headers=headers)
        response.raise_for_status()

        self.json = None

    def info(self):
        """Gets information about the token."""

        assert self.json, (
            '%s needs to call get() method first' % self.__class__.__name__
        )

        url = self.auth_url + '/token/introspect'
        credentials = self.credentials.copy()
        credentials['token'] = self.json['access_token']

        response = requests.post(url=url, data=credentials)
        response.raise_for_status()

        return response.json()

    def __str__(self):
        """Returns the access token as a string."""

        assert self.json, (
            '%s needs to call get() method first' % self.__class__.__name__
        )
        return self.json['access_token']
