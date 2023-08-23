from typing import Dict, Any, Optional
from urllib.parse import urlencode
from requests import Request


class BaseHTTPError(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message


HTTPRequest = Dict[str, Any]


def prepareRequestArgs(request: HTTPRequest) -> Dict[str, Any]:
    url = request["url"]
    if isinstance(url, str):
        url = url.strip()
        if not url.startswith("http"):
            url = "http://" + url
        url = url.split("?", 1)[0]
        if request.get("params"):
            url += "?" + urlencode(request["params"])
    else:
        url = url.geturl()

    headers = request.get("headers") or {}
    body = request.get("body") or {}

    return {"method": request["method"], "url": url, "headers": headers, "data": body}
