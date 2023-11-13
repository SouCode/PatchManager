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

def initiate_download(software_name, download_url, download_directory):
    options = Options()
    options.headless = True
    options.add_experimental_option("prefs", {
        "download.default_directory": download_directory,
        "download.prompt_for_download": False,
    })

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(download_url)

    wait = WebDriverWait(driver, 10)

    if software_name == "Google Chrome":
        download_button = wait.until(EC.element_to_be_clickable((By.ID, "js-download-hero")))
    elif software_name == "Mozilla Firefox":
        download_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div#download-button-thanks a.download-link")))
        direct_download_url = download_button.get_attribute('href')
        driver.get(direct_download_url)
        return

    download_button.click()
    driver.quit()

# Example usage
if __name__ == "__main__":
    download_directory = get_download_directory()
    download_directory = validate_directory(download_directory)

    # Example download URLs (replace with actual URLs as needed)
    chrome_download_url = 'https://www.google.com/chrome/'
    firefox_download_url = 'https://www.mozilla.org/en-US/firefox/new/'

    # Initiate the download process for each software
    initiate_download("Google Chrome", chrome_download_url, download_directory)
    initiate_download("Mozilla Firefox", firefox_download_url, download_directory)
