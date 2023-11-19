import subprocess


def scan_file_with_clamav(file_path):
    try:
        # Run clamscan on the specified file
        result = subprocess.run(['clamscan', file_path], stdout=subprocess.PIPE, text=True)
        output = result.stdout

        # Check the output for the scan result
        if "OK" in output:
            return True  # File is safe
        elif "FOUND" in output:
            return False  # File is infected
        else:
            return None  # Scan was inconclusive or an error occurred
    except Exception as e:
        print(f"An error occurred during antivirus scan: {e}")
        return None
