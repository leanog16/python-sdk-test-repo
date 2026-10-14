"""
webhook_tester.py

Send sample callbacks to a local or tunneled webhook server for testing

@copyright Bandwidth INC
"""
import base64
import json
import ssl
import urllib.request


def send_test_callback(url: str, payload: dict, username: str = "bandwidth",
                       password: str = "changeme123", timeout: float = 10.0) -> int:
    """POST a sample callback payload to a webhook URL

    Self-signed certificates are accepted so this works against local HTTPS
    servers and development tunnels.

    Args:
        url (str): The webhook URL
        payload (dict): The callback JSON to send
        username (str, optional): Basic auth username. Defaults to "bandwidth".
        password (str, optional): Basic auth password. Defaults to "changeme123".
        timeout (float, optional): Request timeout in seconds. Defaults to 10.0.

    Returns:
        int: The HTTP status code returned by the webhook
    """
    credentials = base64.b64encode(f"{username}:{password}".encode()).decode()
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        method="POST",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Basic {credentials}",
            "User-Agent": "bandwidth-webhook-tester",
        },
    )
    context = ssl._create_unverified_context()
    with urllib.request.urlopen(request, timeout=timeout, context=context) as response:
        return response.status
