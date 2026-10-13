# Utilities

The `bandwidth.utils` package contains hand-written helpers that complement the
generated API clients and models.

## Phone numbers

```python
from bandwidth.utils import is_valid_e164, normalize_us_number, to_e164

is_valid_e164("+19195551234")           # True
normalize_us_number("(919) 555-1234")   # "+19195551234"
to_e164("2071838750", default_country_code="44")  # "+442071838750"
```

`normalize_us_number` and `to_e164` raise `InvalidPhoneNumberError` (a
`ValueError` subclass) when the input cannot be converted.

## Callback authentication

If you configure a username and password on your application's callbacks,
Bandwidth sends them using HTTP Basic auth. Verify them in your webhook handler:

```python
from bandwidth.utils import verify_basic_auth_header

if not verify_basic_auth_header(request.headers.get("Authorization"), "user", "pass"):
    return "Unauthorized", 401
```

The comparison is constant time. Missing or malformed headers return `False`.

## Retrying API calls

`retry_with_backoff` retries a function with exponential backoff. `ApiException`
errors are retried only for `429`, `500`, `502`, `503` and `504` by default;
`ConnectionError` and `TimeoutError` are also retried.

```python
from bandwidth.utils import retry_with_backoff

@retry_with_backoff(max_attempts=5, base_delay=1.0)
def send(body):
    return messages_api.create_message(account_id, body)
```

When every attempt fails, `RetryExhaustedError` is raised with `attempts` and
`last_exception` attributes.

| Parameter          | Default                          | Description                                  |
|--------------------|----------------------------------|----------------------------------------------|
| `max_attempts`     | `3`                              | Total attempts including the first           |
| `base_delay`       | `0.5`                            | Delay before the first retry, in seconds     |
| `max_delay`        | `8.0`                            | Upper bound on any single delay              |
| `jitter`           | `True`                           | Randomize each delay between 0 and its value |
| `retry_statuses`   | `(429, 500, 502, 503, 504)`      | HTTP statuses that trigger a retry           |
| `retry_exceptions` | `(ConnectionError, TimeoutError)`| Other exception types that trigger a retry   |
| `on_retry`         | `None`                           | Callback `(attempt, exception, delay)`       |

## Media

```python
from bandwidth.utils import guess_content_type, is_supported_media_type

guess_content_type("cat.jpeg")              # "image/jpeg"
is_supported_media_type("text/plain; charset=utf-8")  # True
```

Unknown extensions fall back to `application/octet-stream`.
