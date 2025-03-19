"""defines helper functions for the fuchs package
to communicate with the hamster and chamaeleon services"""

from typing import Callable
import requests

from . import URL_HAMSTER, URL_CHAMAELEON

def send_request(func: Callable[[], requests.models.Response]):
    try:
        r = func()
        r.raise_for_status()
    except requests.exceptions.HTTPError as http_err:
        return {
            "status": "error",
            "type": "server",
            "message": f"HTTP error occurred: {http_err}",
        }
    except requests.exceptions.RequestException as req_err:
        return {
            "status": "error",
            "type": "server",
            "message": f"Request error occurred: {req_err}",
        }
    except Exception as e:
        return {
            "status": "error",
            "type": "user",
            "message": f"Invalid input: {e}",
        }
    return {"status": "success", "html": r.text}

def put_file_on_hamster(path: str, file):
    url = f"{URL_HAMSTER}/{path}"
    return send_request(lambda: requests.put(url, data=file, timeout=10))

def delete_file_on_hamster(path: str):
    url = f"{URL_HAMSTER}/{path}"
    return send_request(lambda: requests.delete(url, timeout=10))

def convert_md_to_html(md: str):
    """converts markdown to html"""
    url = f"{URL_CHAMAELEON}/"
    return send_request(lambda: requests.post(url, data=md, timeout=10))
