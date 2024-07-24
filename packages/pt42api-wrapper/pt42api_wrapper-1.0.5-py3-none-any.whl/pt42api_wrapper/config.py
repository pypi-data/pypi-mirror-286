import os

sentry = os.getenv('SENTRY_DSN', None)
endpoint = os.getenv('API_ENDPOINT', None)
auth_url = os.getenv('AUTH_URL', None)

credentials = {
    'grant_type': 'client_credentials',
    'client_id': os.getenv('CLIENT_ID', None),
    'client_secret': os.getenv('CLIENT_SECRET', None),
    'scope': 'email profile openid',
}
