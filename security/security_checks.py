import json
import logging
from urllib.parse import urlparse
import requests
from requests.exceptions import SSLError, RequestException


'''
def is_trusted_source(url):
    try:
        with open('config/trusted_sources.json', 'r') as file:
            trusted_sources = json.load(file)["trusted_sources"]
            parsed_url = urlparse(url)
            base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
            return any(base_url.startswith(source) for source in trusted_sources)
    except FileNotFoundError:
        logging.error("Trusted sources configuration file not found.")
        return False
    except json.JSONDecodeError:
        logging.error("Error decoding JSON from the trusted sources file.")
        return False
    except Exception as e:
        logging.error(f"An unexpected error occurred in is_trusted_source: {e}")
        return False
'''

def is_ssl_certificate_valid(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises HTTPError for bad HTTP status codes
        return True
    except SSLError:
        logging.warning(f"SSL error occurred for URL {url}.")
        return False
    except RequestException as e:
        logging.error(f"Request error for URL {url}: {e}")
        return False
    except Exception as e:
        logging.error(f"An unexpected error occurred in is_ssl_certificate_valid: {e}")
        return False
