import json
from models.software import Software
from controllers.blogMonitor import find_chrome_update, find_firefox_update, find_adobe_reader_update, find_zoom_update
from services.downloader import (
    initiate_chrome_download,
    initiate_firefox_download,
    initiate_adobe_acrobat_download,
    initiate_zoom_download,
    get_download_directory,
    validate_directory
)
from security_checks import is_trusted_source


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

        update_found = False
        if software.name == "Google Chrome":
            update_found = find_chrome_update()
            if update_found:
                print(f"New update found for {software.name}. Initiating download...")
                initiate_chrome_download(software.download_url, download_directory)
        elif software.name == "Mozilla Firefox":
            update_found = find_firefox_update()
            if update_found:
                print(f"New update found for {software.name}. Initiating download...")
                initiate_firefox_download(software.download_url, download_directory)
        elif software.name == "Adobe Acrobat":
            update_found = find_adobe_reader_update()
            if update_found:
                print(f"New update found for {software.name}. Initiating download...")
                initiate_adobe_acrobat_download(software.download_url, download_directory)
        elif software.name == "Zoom":
            update_found = find_zoom_update()
            if update_found:
                print(f"New update found for {software.name}. Initiating download...")
                initiate_zoom_download(software.download_url, download_directory)

        if not update_found:
            print(f"No new updates for {software.name}.")

if __name__ == "__main__":
    main()
