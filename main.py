import json
from models.software import Software
from controllers.blogMonitor import find_new_update
from services.downloader import initiate_download, get_download_directory, validate_directory

# Function to load the list of software from the JSON configuration file
def load_software_list():
    # Open the JSON file containing software configurations
    with open('config/software_list.json', 'r') as file:
        # Load the JSON data from the file
        software_data = json.load(file)
        # Create and return a list of Software objects from the JSON data
        return [Software(**software) for software in software_data]

# The main function where the program execution begins
def main():
    # Load the list of software from the JSON configuration
    software_list = load_software_list()

    # Prompt the user to enter the download directory path
    download_directory = get_download_directory()
    # Validate the provided directory path and create it if necessary
    download_directory = validate_directory(download_directory)

    # Iterate over each software in the list
    for software in software_list:
        # Print a message indicating that the program is checking for updates
        print(f"Checking for updates for {software.name}...")

        # Check if the software is Google Chrome and if a new update is available
        if software.name == "Google Chrome" and find_new_update():
            # Print a message indicating that a new update was found and is being downloaded
            print(f"New update found for {software.name}. Initiating download...")
            # Initiate the download process for the software
            initiate_download(software.download_url, download_directory)
        else:
            # Print a message indicating that no new updates were found for the software
            print(f"No new updates for {software.name}.")

# Check if the script is being run directly (not imported as a module)
if __name__ == "__main__":
    # If the script is run directly, execute the main function
    main()

