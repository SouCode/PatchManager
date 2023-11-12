import requests
from bs4 import BeautifulSoup

# Function to check for new updates on the Google Chrome blog
def find_new_update():
    # URL of the Google Chrome releases blog
    url = 'https://chromereleases.googleblog.com/'

    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.ok:
        # Get the HTML content of the page
        html = response.text

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')

        # Iterate over each post title on the blog
        # Assuming each post title is in an 'a' tag within an 'h2' with class 'title'
        for title in soup.find_all('h2', class_='title'):
            # Find the 'a' tag within the title
            a_tag = title.find('a')

            # Check if the 'a' tag exists and contains the specific update text
            if a_tag and "Beta Channel Update for ChromeOS / ChromeOS Flex" in a_tag.text:
                # Return True if the specific update is found
                return True

    # Return False if the update is not found or if the request was not successful
    return False
