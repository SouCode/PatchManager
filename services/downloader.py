import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Function to get the download directory path from the user
def get_download_directory():
    print("Please enter the download directory path.")
    directory = input("Download Directory: ").strip()
    return directory

# Function to validate the existence of the directory
def validate_directory(directory):
    # Check if the directory does not exist
    if not os.path.exists(directory):
        # Ask the user if they want to create the directory
        create = input(f"The directory '{directory}' does not exist. Create it? (y/n): ").lower()
        if create == 'y':
            # Create the directory
            os.makedirs(directory, exist_ok=True)
            print(f"Directory '{directory}' created.")
        else:
            # Exit the program if the user chooses not to create the directory
            print("Exiting program.")
            exit()
    # Check if the provided path is not a directory
    elif not os.path.isdir(directory):
        print(f"The path '{directory}' is not a directory.")
        exit()
    return directory

# Function to initiate the download process
def initiate_download(download_url, download_directory):
    # Set options for the Chrome driver
    options = Options()
    options.headless = True  # Run Chrome in headless mode (no GUI)
    options.add_experimental_option("prefs", {
        "download.default_directory": download_directory,  # Set the default download directory
        "download.prompt_for_download": False,  # Disable download prompt
    })

    # Set up the Chrome driver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(download_url)  # Navigate to the download URL

    # Wait for the download button to be clickable and then click it
    wait = WebDriverWait(driver, 10)
    download_button = wait.until(EC.element_to_be_clickable((By.ID, "js-download-hero")))
    download_button.click()

    driver.quit()  # Close the browser

# Get the download directory from the user
download_directory = get_download_directory()
# Validate the download directory
download_directory = validate_directory(download_directory)

# Example download URL (replace with the actual URL)
download_url = 'https://www.google.com/chrome/'

# Initiate the download process
initiate_download(download_url, download_directory)
