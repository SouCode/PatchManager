import requests
from bs4 import BeautifulSoup
from datetime import datetime
from requests import RequestException


def find_chrome_update():
    chrome_blog_url = 'https://chromereleases.googleblog.com/'
    chrome_update_text = "Beta Channel Release for ChromeOS / ChromeOS Flex"
    version_prefix = "The Beta channel has been updated to"

    try:
        response = requests.get(chrome_blog_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            for post in soup.find_all('div', class_='post'):
                title = post.find('h2', class_='title')
                if title and chrome_update_text in title.get_text():
                    date_tag = post.find('span', class_='publishdate')
                    date_text = date_tag.get_text(strip=True) if date_tag else "Unknown Date"

                    content_div = post.find('div', class_='post-content post-original')
                    if content_div:
                        if version_prefix in content_div.get_text():
                            version_info = content_div.find('span', style="color: black; white-space-collapse: preserve;").get_text(strip=True)
                            return True, date_text, version_info

        else:
            print(f"Unexpected status code: {response.status_code}")
    except RequestException as e:
        print(f"Request failed: {e}")

    return False, None, None
def find_firefox_update():
    # URL of the Mozilla Firefox announcement group
    firefox_blog_url = 'https://groups.google.com/g/mozilla.announce'
    # Text to identify the specific update we're looking for
    firefox_update_text = "Firefox update is now available"

    try:
        # Attempt to send a GET request to the Firefox announcement group URL
        response = requests.get(firefox_blog_url)

        # Check if the response status code is 200 (OK)
        if response.status_code == 200:
            # Parse the HTML content of the response
            soup = BeautifulSoup(response.text, 'html.parser')

            # Use CSS selectors to find the specific posts we're interested in
            for post in soup.select('span.eois5 div.y7VPke a.ZLl54'):
                # Find the span element containing the post title
                post_title = post.select_one('span.o1DPKc')

                # Check if the post title exists and contains the specific update text
                if post_title and firefox_update_text in post_title.text:
                    # Return True if the specific update is found
                    return True
        else:
            # Print an error message if the status code is not 200
            print(f"Unexpected status code: {response.status_code}")
    except RequestException as e:
        # Print an error message if a network error occurs
        print(f"Request failed: {e}")
    except Exception as e:
        # Print an error message if a parsing error occurs
        print(f"An error occurred during parsing: {e}")

    # Return False if the update is not found or if an error occurred
    return False


def find_adobe_reader_update():
    # Define the URL for Adobe Acrobat Reader DC release notes
    adobe_reader_blog_url = 'https://www.adobe.com/devnet-docs/acrobatetk/tools/ReleaseNotesDC/index.html'

    try:
        # Attempt to send a GET request to the Adobe Reader release notes URL
        response = requests.get(adobe_reader_blog_url)

        # Check if the response status code is 200 (OK)
        if response.status_code == 200:
            # Parse the HTML content of the response
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find the first <li> element in the <ul class="simple"> list
            first_li = soup.select_one('ul.simple li')
            if first_li:
                # Extract the text from the first <li> element
                first_li_text = first_li.get_text(strip=True)

                # You can add logic here to determine if the text indicates a new update
                # For example, checking if the date in the text is more recent than a certain date
                # For simplicity, let's assume any found text indicates a new update
                return True
        else:
            # Print an error message if the status code is not 200
            print(f"Unexpected status code: {response.status_code}")
    except RequestException as e:
        # Print an error message if a network error occurs
        print(f"Request failed: {e}")
    except Exception as e:
        # Print an error message if a parsing error occurs
        print(f"An error occurred during parsing: {e}")

    # Return False if no new update is found or if an error occurred
    return False


def find_zoom_update():
    # URL of the Zoom support page for release notes
    zoom_blog_url = 'https://support.zoom.com/hc/en/category?id=kb_category&kb_category=f55a321e8720391089a37408dabb35fa'

    try:
        # Attempt to send a GET request to the Zoom support page
        response = requests.get(zoom_blog_url)

        # Check if the response status code is 200 (OK)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find the list of articles
            articles_list = soup.find('ul', class_='parent-category-articles article-list-ul')
            if articles_list:
                # Iterate through the articles to find the newest one
                for article in articles_list.find_all('li', {'ng-repeat': 'article in data.thisCategoriesArticles'}):
                    article_link = article.find('a')
                    if article_link:
                        # Extract the date from the article title
                        article_title = article_link.text.strip()
                        if "Release notes for" in article_title:
                            # Extract the date from the title and convert it to a datetime object
                            release_date_str = article_title.replace("Release notes for ", "")
                            release_date = datetime.strptime(release_date_str, "%B %d, %Y")

                            # Compare the release date with the current date
                            if release_date.date() > datetime.now().date():
                                return True
        else:
            # Print an error message if the status code is not 200
            print(f"Unexpected status code: {response.status_code}")
    except RequestException as e:
        # Print an error message if a network error occurs
        print(f"Request failed: {e}")
    except Exception as e:
        # Print an error message if a parsing error occurs
        print(f"An error occurred during parsing: {e}")

    # Return False if no new update is found or if an error occurred
    return False

update_found, update_date, update_info = find_chrome_update()
if update_found:
    print(f"Update found on {update_date}: {update_info}")
else:
    print("No update found.")