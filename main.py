from services.downloader import (
    initiate_chrome_download,
    initiate_firefox_download,
    initiate_adobe_acrobat_download,
    initiate_zoom_download,
    get_download_directory,
    validate_directory
)
from controllers.blogMonitor import (
    find_and_extract_chrome_update,
    find_firefox_update,
    find_adobe_reader_update,
    find_zoom_update
)


def main():
    download_directory = get_download_directory()
    download_directory = validate_directory(download_directory)

    # Google Chrome Update Check and Download
    chrome_download_url = 'https://chromeenterprise.google/browser/download/#windows-tab'
    if find_and_extract_chrome_update():
        print("New update found for Google Chrome. Initiating download...")
        initiate_chrome_download(chrome_download_url, download_directory, '64bit')
        initiate_chrome_download(chrome_download_url, download_directory, '32bit')
    '''
    # Mozilla Firefox Update Check and Download
    firefox_download_url = 'https://www.mozilla.org/en-US/firefox/new/'
    if find_firefox_update():
        print("New update found for Mozilla Firefox. Initiating download...")
        initiate_firefox_download(firefox_download_url, download_directory)

    # Adobe Acrobat Update Check and Download
    adobe_acrobat_download_url = 'https://www.adobe.com/devnet-docs/acrobatetk/tools/ReleaseNotesDC/continuous/dccontinuousnov2023.html#dccontinuousnovtwentytwentythree'
    if find_adobe_reader_update():
        print("New update found for Adobe Acrobat. Initiating download...")
        initiate_adobe_acrobat_download(adobe_acrobat_download_url, download_directory)

    # Zoom Update Check and Download
    zoom_download_url = 'https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0060407#collapsePC'
    if find_zoom_update():
        print("New update found for Zoom. Initiating download...")
        initiate_zoom_download(zoom_download_url, download_directory, "32bit")
        initiate_zoom_download(zoom_download_url, download_directory, "64bit")
    '''


if __name__ == "__main__":
    main()
