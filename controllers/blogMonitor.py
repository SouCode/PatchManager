import requests
from bs4 import BeautifulSoup
from datetime import datetime
from requests import RequestException


def find_firefox_update():
    firefox_releases_url = 'https://www.mozilla.org/en-US/firefox/releases/'

    try:
        response = requests.get(firefox_releases_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            release_list = soup.find('ol', class_='c-release-list')
            if release_list:
                latest_release = release_list.find('li')
                if latest_release:
                    main_version = latest_release.strong.a.get_text()
                    print(f"Latest Firefox version: {main_version}")

                    # Check for sub-versions
                    sub_versions = latest_release.find('ol')
                    if sub_versions:
                        for sub_version in sub_versions.find_all('li'):
                            print(f"Sub-version: {sub_version.a.get_text()}")
        else:
            print(f"Unexpected status code: {response.status_code}")
    except RequestException as e:
        print(f"Request failed: {e}")
    except Exception as e:
        print(f"An error occurred during parsing: {e}")


find_firefox_update()


def find_adobe_reader_update():
    adobe_reader_blog_url = 'https://www.adobe.com/devnet-docs/acrobatetk/tools/ReleaseNotesDC/index.html'

    try:
        response = requests.get(adobe_reader_blog_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            first_li = soup.select_one('ul.simple li')
            if first_li:
                first_li_text = first_li.get_text(strip=True)
                print(f"Latest Adobe Reader update: {first_li_text}")
        else:
            print(f"Unexpected status code: {response.status_code}")
    except RequestException as e:
        print(f"Request failed: {e}")
    except Exception as e:
        print(f"An error occurred during parsing: {e}")


find_adobe_reader_update()


def find_zoom_update():
    zoom_blog_url = 'https://support.zoom.com/hc/en/category?id=kb_category&kb_category=f55a321e8720391089a37408dabb35fa'

    try:
        response = requests.get(zoom_blog_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Adjust the selector to target the specific <ul> within the nested structure
            target_div = soup.find('div', id='x883eb8f887c5751089a37408dabb35bc')
            if target_div:
                ul_element = target_div.find('ul', class_='parent-category-articles article-list-ul')
                if ul_element:
                    first_li = ul_element.find('li', class_='ng-scope')
                    if first_li:
                        article_link = first_li.find('a', class_='ng-binding')
                        if article_link and "Release notes for" in article_link.text:
                            release_info = article_link.text.strip()
                            print(f"New Zoom update found: {release_info}")
                            return
            else:
                print("Target div not found.")
        else:
            print(f"Unexpected status code: {response.status_code}")
    except RequestException as e:
        print(f"Request failed: {e}")
    except Exception as e:
        print(f"An error occurred during parsing: {e}")

    print("No new Zoom updates found.")

# Call the function
find_zoom_update()


def find_and_extract_chrome_update():
    chrome_blog_url = 'https://chromereleases.googleblog.com/search?max-results=20'
    chrome_update_text = "Beta Channel Release for ChromeOS / ChromeOS Flex"

    try:
        while True:
            response = requests.get(chrome_blog_url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')

                for post in soup.find_all('div', class_='post'):
                    title = post.find('h2', class_='title')
                    if title and chrome_update_text in title.get_text():
                        date_text = post.find('span', class_='publishdate').get_text(strip=True)
                        update_info = extract_update_info_from_post(post)
                        if update_info:
                            print(f"Update found on {date_text}: {update_info}")
                            return
                        else:
                            print("Update information not found.")
                            return

                # Check for a link to the next page
                older_link = soup.find('a', string='Older Posts')
                if older_link and 'href' in older_link.attrs:
                    chrome_blog_url = older_link['href']  # Update the URL for the next page
                else:
                    break  # Exit the loop if there are no more pages
            else:
                print(f"Unexpected status code: {response.status_code}")
                break

    except RequestException as e:
        print(f"Request failed: {e}")

    print("No update found.")


def extract_update_info_from_post(post):
    search_phrase = "The Beta channel has been updated to"
    post_body_div = post.find('div', class_='post-body')
    if post_body_div:
        paragraphs = post_body_div.find_all('p')
        for p in paragraphs:
            if search_phrase in p.get_text():
                update_info = p.get_text(strip=True)
                update_info = update_info.replace("updated to", "updated to ")
                platform_version_index = update_info.find("(Platform version:")
                if platform_version_index != -1:
                    update_info = update_info[:platform_version_index].strip() + " for ChromeOS devices."
                return update_info
    return None


# Call the function
find_and_extract_chrome_update()
