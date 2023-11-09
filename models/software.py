
class Software:
    def __init__(self, name, current_version, update_url, download_url=None):
        self.name = name
        self.current_version = current_version
        self.update_url = update_url
        self.download_url = download_url

    def __str__(self):
        return f"{self.name} - Current Version: {self.current_version}"

    def check_for_update(self):
        # I will later add a way to check for updates from the update_url
        pass

    def download_update(self):
        # I will expand this to download updates from the download_url
        pass
