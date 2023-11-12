import json
from models.software import Software
from controllers.blogMonitor import find_new_update
from services.downloader import initiate_download, get_download_directory, validate_directory


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
        if software.name == "Google Chrome" and find_new_update():
            print(f"New update found for {software.name}. Initiating download...")
            initiate_download(software.download_url, download_directory)
        else:
            print(f"No new updates for {software.name}.")


if __name__ == "__main__":
    main()
