import requests
from bs4 import BeautifulSoup


def find_new_update():
    url = 'https://chromereleases.googleblog.com/'
    response = requests.get(url)
    if response.ok:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        # Assuming each post title is in an 'a' tag within an 'h2' with class 'title'
        for title in soup.find_all('h2', class_='title'):
            a_tag = title.find('a')
            if a_tag and "Beta Channel Update for ChromeOS / ChromeOS Flex" in a_tag.text:
                return True
    return False
