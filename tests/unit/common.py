"""
Common functions for tests
"""


def get_payload(post_message):
    """
    Retrieve test payload
    """
    payload = {}
    payload["web_client"] = type("", (), {})()
    payload["web_client"].chat_postMessage = post_message
    payload["data"] = {}
    payload["data"]["user"] = "test"
    payload["data"]["channel"] = "test"
    payload["data"]["ts"] = "test"
    return payload
