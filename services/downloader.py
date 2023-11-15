import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


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


def initiate_chrome_download(download_url, download_directory, architecture):
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

    # Select MSI file type

    msi_dropdown = wait.until(EC.element_to_be_clickable((By.ID, "selectedtext-WINFiletype")))
    msi_dropdown.click()
    msi_option = wait.until(EC.element_to_be_clickable((By.XPATH, "//li[@data-value='msi']")))
    msi_option.click()

    # Select architecture (64-bit or 32-bit)
    arch_dropdown = wait.until(EC.element_to_be_clickable((By.ID, "selectedtext-Architecture")))
    arch_dropdown.click()
    arch_option = wait.until(EC.element_to_be_clickable((By.XPATH, f"//li[@data-value='{architecture}']")))
    arch_option.click()

    # Click the download button
    download_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.ce-download__download-dlbutton")))
    download_button.click()

    # Wait for download to complete
    time.sleep(10)  # Adjust this time as needed

    driver.quit()


def initiate_firefox_download(download_url, download_directory):
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
    download_button = wait.until(EC.element_to_be_clickable((By.ID, "download-button-thanks")))
    download_button.click()

    # Wait for download to complete
    time.sleep(10)  # Adjust this time as needed

    driver.quit()

def initiate_adobe_acrobat_download(download_page_url, download_directory):
    options = Options()
    options.headless = True
    options.add_experimental_option("prefs", {
        "download.default_directory": download_directory,
        "download.prompt_for_download": False,
    })

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(download_page_url)

    wait = WebDriverWait(driver, 10)

    # Locate the 32-bit installer link
    installer_32bit = wait.until(EC.presence_of_element_located(
        (By.XPATH, "(//div[@class='wy-table-responsive'])[1]//tbody/tr[@class='row-even']/td[3]/p/a")))
    installer_32bit_url = installer_32bit.get_attribute('href')

    # Locate the 64-bit installer link
    installer_64bit = wait.until(EC.presence_of_element_located(
        (By.XPATH, "(//div[@class='wy-table-responsive'])[2]//tbody/tr[@class='row-even']/td[3]/p/a")))
    installer_64bit_url = installer_64bit.get_attribute('href')

    # Download the 32-bit installer
    driver.get(installer_32bit_url)
    time.sleep(10)  # Adjust this time as needed

    # Download the 64-bit installer
    driver.get(installer_64bit_url)
    time.sleep(10)  # Adjust this time as needed

    driver.quit()



download_directory = get_download_directory()
download_directory = validate_directory(download_directory)

# Download Google Chrome
chrome_download_url = 'https://chromeenterprise.google/browser/download/#windows-tab'
initiate_chrome_download(chrome_download_url, download_directory, '64')
initiate_chrome_download(chrome_download_url, download_directory, '32')

# Download Firefox
firefox_download_url = 'https://www.mozilla.org/en-US/firefox/new/'
initiate_firefox_download(firefox_download_url, download_directory)

# Download Adobe Reader
adobe_acrobat_page_url = 'https://www.adobe.com/devnet-docs/acrobatetk/tools/ReleaseNotesDC/continuous/dccontinuousnov2023.html#dccontinuousnovtwentytwentythree'
initiate_adobe_acrobat_download(adobe_acrobat_page_url, download_directory)