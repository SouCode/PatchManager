import requests
from bs4 import BeautifulSoup


def find_chrome_update():
    # URL of the Google Chrome releases blog
    chrome_blog_url = 'https://chromereleases.googleblog.com/'
    # Text to identify the specific update we're looking for
    chrome_update_text = "Beta Channel Update for ChromeOS / ChromeOS Flex"

    # Send a GET request to the Chrome blog URL
    response = requests.get(chrome_blog_url)
    # Check if the request was successful
    if response.ok:
        # Parse the HTML content of the response
        soup = BeautifulSoup(response.text, 'html.parser')
        # Iterate over each post title on the blog
        for post in soup.find_all('h2', class_='title'):
            # Find the 'a' tag within the post title
            a_tag = post.find('a')
            # Check if the 'a' tag exists and contains the specific update text
            if a_tag and chrome_update_text in a_tag.text:
                # Return True if the specific update is found
                return True
    # Return False if the update is not found or if the request was not successful
    return False


def find_firefox_update():
    # URL of the Mozilla Firefox announcement group
    firefox_blog_url = 'https://groups.google.com/g/mozilla.announce'
    # Text to identify the specific update we're looking for
    firefox_update_text = "Firefox update is now available"

    # Send a GET request to the Firefox announcement group URL
    response = requests.get(firefox_blog_url)
    # Check if the request was successful
    if response.ok:
        # Parse the HTML content of the response
        soup = BeautifulSoup(response.text, 'html.parser')
        # Use CSS selectors to find the specific posts we're interested in
        for post in soup.select('span.eois5 div.y7VPke a.ZLl54'):
            # Find the span element containing the post title
            post_title = post.select_one('span.o1DPKc') #fix this !!!!
            # Check if the post title exists and contains the specific update text
            if post_title and firefox_update_text in post_title.text:
                # Return True if the specific update is found
                return True
    # Return False if the update is not found or if the request was not successful
    return False
