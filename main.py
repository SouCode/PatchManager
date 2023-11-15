import json
from models.software import Software
from controllers.blogMonitor import find_chrome_update, find_firefox_update
from services.downloader import initiate_chrome_download, initiate_firefox_download, get_download_directory, validate_directory

def load_software_list():
    with open('config/software_list.json', 'r') as file:
        software_data = json.load(file)
        return [Software(**software) for software in software_data]

def main():
    software_list = load_software_list()
    download_directory = get_download_directory()
    download_directory = validate_directory(download_directory)

    for software in software_list:
        print(f"Checking for updates for {software.name}...")

        if software.name == "Google Chrome":
            if find_chrome_update():
                print(f"New update found for {software.name}. Initiating download...")
                chrome_download_url = 'https://chromeenterprise.google/browser/download/#windows-tab'
                initiate_chrome_download(chrome_download_url, download_directory, '64')
                initiate_chrome_download(chrome_download_url, download_directory, '32')
            else:
                print(f"No new updates for {software.name}.")

        elif software.name == "Mozilla Firefox":
            if find_firefox_update():
                print(f"New update found for {software.name}. Initiating download...")
                firefox_download_url = 'https://www.mozilla.org/en-US/firefox/new/'
                initiate_firefox_download(firefox_download_url, download_directory)
                # get all versions https://www.mozilla.org/en-US/firefox/all/#product-desktop-release
            else:
                print(f"No new updates for {software.name}.")

if __name__ == "__main__":
    main()

