"""Reading the Retry-After header a provider sends with a rate-limit response.

The router uses this to decide how long to keep an account in cooldown before
trying it again.
"""


def parse_retry_after(headers):
    """Seconds to wait before retrying, or None if the header is absent."""
    value = headers.get("retry-after")
    if value is None:
        return None
    return int(value)
