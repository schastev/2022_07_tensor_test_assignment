import requests


def download_bytes(link):
    return requests.get(link).content
