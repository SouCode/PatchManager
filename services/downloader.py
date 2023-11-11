import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_download_directory():
    print("Please enter the download directory path.")
    directory = input("Download Directory: ").strip()
    return directory


def validate_directory(directory):
    if not os.path.exists(directory):
        create = input(f"The directory '{directory}' does not exist. Create it? (y/n): ").lower()
        if create == 'y':
            os.makedirs(directory, exist_ok=True)
            print(f"Directory '{directory}' created.")
        else:
            print("Exiting program.")
            exit()
    elif not os.path.isdir(directory):
        print(f"The path '{directory}' is not a directory.")
        exit()
    return directory


def initiate_download(download_url, download_directory):
    options = Options()
    options.headless = True
    options.add_experimental_option("prefs", {
        "download.default_directory": download_directory,
        "download.prompt_for_download": False,
    })

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(download_url)

    # Replace the below line with the actual method to find the download button or link
    wait = WebDriverWait(driver, 10)
    download_button = wait.until(EC.element_to_be_clickable((By.ID, "js-download-hero")))
    download_button.click()

    driver.quit()


download_directory = get_download_directory()
download_directory = validate_directory(download_directory)

# Example download URL (replace with the actual URL)
download_url = 'https://www.google.com/chrome/'

initiate_download(download_url, download_directory)
