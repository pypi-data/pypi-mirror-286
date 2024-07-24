# pt42api_wrapper

A python package that simplifies the process of making API requests to 42 Portugal's API. With this package, developers can quickly and easily access the API's functionality, without having to deal with the complexities of working directly with it.

## How to install

```shell
pip install pt42api-wrapper
```

## Making a simple request

- Have a `.env` file that looks like this:

```shell
export API_ENDPOINT=''
export AUTH_URL=''
export CLIENT_ID=''
export CLIENT_SECRET=''
export SENTRY_DSN=''
```

- Use the following code to make a simple request:

```python
import pt42api_wrapper as pt42api

api = pt42api.ApiWrapper()
api.get(url='campus/')
```

## Using in Django Projects

```python
# settings.py
...
PT42API_WRAPPER = {
    'base_url': os.environ.get('API_ENDPOINT'),
    'auth_url': os.environ.get('AUTH_URL'),
    'client_id': os.environ.get('CLIENT_ID'),
    'client_secret': os.environ.get('CLIENT_SECRET'),
    'sentry_dsn': os.environ.get('SENTRY_DSN')
}
```

```python
from django.conf import settings

import pt42api_wrapper as pt42api

(...)

api = pt42api.ApiWrapper(**settings.PT42API_WRAPPER)
url = f'{self.request_url}{data.get("id")}/'
response = api.delete(url, data)
return http.JsonResponse(response.json(), status=response.status_code)

(...)
```

## Configure Api log level

```python
from pt42-wrapper import ApiWrapper

(...)

api = ApiWrapper(log_level=logging.DEBUG)

(...)
```

## Running tests

```shell
python3 tests.py
```
