import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from ..security.antivirus_scan import scan_file_with_clamav

import os


def get_download_directory():
    while True:
        print("Please enter the download directory path.")
        directory = input("Download Directory: ").strip()

        # Check if the directory path is empty
        if not directory:
            print("The directory path cannot be empty. Please enter a valid path.")
            continue

        # Check if the path exists and is a directory
        if os.path.exists(directory) and os.path.isdir(directory):
            # Check if the directory is writable
            if os.access(directory, os.W_OK):
                return directory
            else:
                print(f"The directory '{directory}' is not writable. Please enter a different path.")
        else:
            create = input(f"The directory '{directory}' does not exist. Create it? (y/n): ").lower()
            if create == 'y':
                try:
                    os.makedirs(directory, exist_ok=True)
                    print(f"Directory '{directory}' created.")
                    return directory
                except OSError as e:
                    print(f"Failed to create the directory: {e}")
            else:
                print("Please enter a valid directory path.")

        # If the directory is not valid, the loop will continue asking for a valid path


def validate_directory(directory):
    try:
        if not os.path.exists(directory):
            create = input(f"The directory '{directory}' does not exist. Create it? (y/n): ").lower()
            if create == 'y':
                os.makedirs(directory, exist_ok=True)
                print(f"Directory '{directory}' created.")
            else:
                print("Exiting program.")
                sys.exit()
        elif not os.path.isdir(directory):
            print(f"The path '{directory}' is not a directory.")
            sys.exit()
        else:
            # Check if the directory is writable
            if not os.access(directory, os.W_OK):
                print(f"The directory '{directory}' is not writable. Please provide a writable directory.")
                sys.exit()
        return directory
    except OSError as e:
        print(f"An error occurred while validating the directory: {e}")
        sys.exit()


def handle_scan_result(scan_result, file_path):
    if scan_result is None:
        print(f"Scan was inconclusive or an error occurred for file: {file_path}.")
    elif not scan_result:
        print(f"Warning: The file {file_path} is infected. Action is required.")
    else:
        print(f"The file {file_path} is safe.")


def initiate_chrome_download(download_url, download_directory, architecture="64-bit"):
    driver = None
    try:
        options = Options()
        options.headless = True
        options.add_experimental_option("prefs", {
            "download.default_directory": download_directory,
            "download.prompt_for_download": False,
        })

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.set_window_size(1200, 800)  # Set a larger window size

        driver.get(download_url)
        wait = WebDriverWait(driver, 10)

        # Click the specified div to open the dropdown
        msi_dropdown_div = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/main/section[2]/div/div[2]/div[1]/div[2]/div/div[1]/div/div[5]/div/div[2]/div/div/div[1]")))
        msi_dropdown_div.click()

        # Wait and click the specific MSI option in the dropdown
        msi_option = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/main/section[2]/div/div[2]/div[1]/div[2]/div/div[1]/div/div[5]/div/div[2]/div/div/div[2]/ul/li[2]")))
        msi_option.click()

        # Wait for any overlays to disappear
        wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.overlay")))

        # If architecture is 32-bit, change the selection
        if architecture == "32-bit":
            arch_dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/main/section[2]/div/div[2]/div[1]/div[2]/div/div[1]/div/div[5]/div/div[3]/div/div/div[1]/span[3]/span[2]")))
            arch_dropdown.click()
            arch_option = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/main/section[2]/div/div[2]/div[1]/div[2]/div/div[1]/div/div[5]/div/div[3]/div/div/div[2]/ul/li[2]")))
            arch_option.click()

        # Click the download button
        download_button = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/main/section[2]/div/div[2]/div[1]/div[2]/div/div[1]/div/div[5]/div/div[4]/a[2]")))
        download_button.click()

        # Wait for download to complete
        time.sleep(10)  # Adjust this time as needed

        # Assuming the file name is known or can be determined
        downloaded_file_path = os.path.join(download_directory, "chrome_installer.msi")
        # scan_result = scan_file_with_clamav(downloaded_file_path)
        # handle_scan_result(scan_result, downloaded_file_path)

    except Exception as e:
        print(f"An error occurred during the download process: {e}")
    finally:
        if driver:
            driver.quit()


'''
def initiate_firefox_download(download_url, download_directory):
    driver = None  # Initialize driver to None
    try:
        # SSL and source checks
        if not is_trusted_source(download_url) or not is_ssl_certificate_valid(download_url):
            print("Download URL is not safe.")
            return

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

        # Assuming the file name is known or can be determined
        downloaded_file_path = os.path.join(download_directory, "firefox_installer.exe")
        scan_result = scan_file_with_clamav(downloaded_file_path)
        handle_scan_result(scan_result, downloaded_file_path)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if driver:
            driver.quit()


def initiate_adobe_acrobat_download(download_page_url, download_directory):
    driver = None  # Initialize driver to None
    try:
        # SSL and source checks
        if not is_trusted_source(download_page_url) or not is_ssl_certificate_valid(download_page_url):
            print("Download URL is not safe.")
            return

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

        # Assuming the file names are known or can be determined
        downloaded_file_path_32bit = os.path.join(download_directory, "adobe_reader_32bit_installer.exe")
        scan_result_32bit = scan_file_with_clamav(downloaded_file_path_32bit)
        handle_scan_result(scan_result_32bit, downloaded_file_path_32bit)

        downloaded_file_path_64bit = os.path.join(download_directory, "adobe_reader_64bit_installer.exe")
        scan_result_64bit = scan_file_with_clamav(downloaded_file_path_64bit)
        handle_scan_result(scan_result_64bit, downloaded_file_path_64bit)

    except Exception as e:
        print(f"An error occurred during the download process: {e}")
    finally:
        if driver:
            driver.quit()


def initiate_zoom_download(download_url, download_directory, arch_type):
    driver = None  # Initialize driver to None
    try:
        # SSL and source checks
        if not is_trusted_source(download_url) or not is_ssl_certificate_valid(download_url):
            print("Download URL is not safe.")
            return

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
        # Wait for the panel to be visible and click to expand if necessary
        panel = wait.until(EC.visibility_of_element_located((By.ID, "collapsePC")))
        if not panel.get_attribute('class').endswith('in'):
            driver.find_element(By.ID, "collapsePC").click()

        # Wait for the list of download links to be visible
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.panel-body ul")))

        # Select the correct download link based on architecture type
        if arch_type == "32bit":
            download_link = driver.find_element(By.CSS_SELECTOR, "div.panel-body ul li:first-child a")
        else:  # 64bit
            download_link = driver.find_element(By.CSS_SELECTOR, "div.panel-body ul li:nth-child(2) a")

        download_link.click()

        # Wait for download to complete
        time.sleep(10)

        # Assuming the file name is known or can be determined
        downloaded_file_path = os.path.join(download_directory, f"zoom_installer_{arch_type}.exe")
        scan_result = scan_file_with_clamav(downloaded_file_path)
        handle_scan_result(scan_result, downloaded_file_path)

    except Exception as e:
        print(f"An error occurred during the download process: {e}")
    finally:
        if driver:
            driver.quit()

'''
download_directory = get_download_directory()
download_directory = validate_directory(download_directory)

# Download Google Chrome
chrome_download_url = 'https://chromeenterprise.google/browser/download/#windows-tab'
initiate_chrome_download(chrome_download_url, download_directory, '64')
initiate_chrome_download(chrome_download_url, download_directory, '32')

'''
# Download Firefox
firefox_download_url = 'https://www.mozilla.org/en-US/firefox/new/'
initiate_firefox_download(firefox_download_url, download_directory)

# Download Adobe Reader
adobe_acrobat_page_url = 'https://www.adobe.com/devnet-docs/acrobatetk/tools/ReleaseNotesDC/continuous/dccontinuousnov2023.html#dccontinuousnovtwentytwentythree'
initiate_adobe_acrobat_download(adobe_acrobat_page_url, download_directory)

# Download Zoom
zoom_download_url = 'https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0060407#collapsePC'
initiate_zoom_download(zoom_download_url, download_directory, "32bit")
initiate_zoom_download(zoom_download_url, download_directory, "64bit")
'''