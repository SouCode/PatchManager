import subprocess
import logging


def test_scan_file_with_clamav(file_path):
    try:
        # Run clamscan on the specified file
        result = subprocess.run(['clamscan', file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output = result.stdout

        # Check the output for the scan result
        if "OK" in output:
            return True  # File is safe
        elif "FOUND" in output:
            return False  # File is infected
        else:
            logging.warning(f"Scan inconclusive or error occurred. Output: {output}")
            return None  # Scan was inconclusive or an error occurred
    except subprocess.CalledProcessError as e:
        # Handle errors related to the subprocess call
        logging.error(f"Subprocess error during antivirus scan: {e}")
        return None
    except FileNotFoundError:
        # Handle the case where clamscan is not installed
        logging.error("ClamAV is not installed or clamscan is not in the PATH.")
        return None
    except Exception as e:
        # Handle any other exceptions
        logging.error(f"An unexpected error occurred during antivirus scan: {e}")
        return None
