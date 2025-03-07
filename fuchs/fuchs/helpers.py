"""defines helper functions for the fuchs package
to communicate with the hamster and chamaeleon services"""

import requests

from . import URL_HAMSTER, URL_CHAMAELEON


def put_file_on_hamster(path: str, file):
    url = f"{URL_HAMSTER}/{path}"
    r = requests.put(url, data=file, timeout=10)
    assert r.status_code == 200, f"status: {r.status_code}\nmessage: {r.text}"


def delete_file_on_hamster(path: str):
    url = f"{URL_HAMSTER}/{path}"
    r = requests.delete(url, timeout=10)
    assert r.status_code == 200, f"status: {r.status_code}\nmessage: {r.text}"


def convert_md_to_html(md: str) -> str:
    """converts markdown to html"""
    r = requests.post(f"{URL_CHAMAELEON}/", data=md, timeout=10)
    assert r.status_code == 200
    return r.text
