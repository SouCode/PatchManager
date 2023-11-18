# security_checks.py
import json
from urllib.parse import urlparse
import requests
from requests.exceptions import SSLError


def is_trusted_source(url):
    with open('config/trusted_sources.json', 'r') as file:
        trusted_sources = json.load(file)["trusted_sources"]
        parsed_url = urlparse(url)
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
        return any(base_url.startswith(source) for source in trusted_sources)


def is_ssl_certificate_valid(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises HTTPError for bad HTTP status codes
        return True
    except SSLError:
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
