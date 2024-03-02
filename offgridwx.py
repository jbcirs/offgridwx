import requests
import os
import shutil
import sys

def empty_folder(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')

def download_file(shortcode, output_folder):
    base_url = "https://ogwx.info/"
    url = f"{base_url}{shortcode}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        content_type = response.headers['Content-Type']

        if 'text/plain' in content_type:
            extension = '.txt'
        elif 'application/json' in content_type:
            extension = '.json'
        elif 'text/csv' in content_type:
            extension = '.csv'
        elif 'application/pdf' in content_type:
            extension = '.pdf'
        else:
            extension = '.txt'

        file_path = os.path.join(output_folder, f"{shortcode}{extension}")

        with open(file_path, 'wb') as file:
            file.write(response.content)

        print(f"File downloaded successfully: {file_path}")

    except requests.exceptions.HTTPError as err:
        print(f"HTTP Error: {err}")
    except requests.exceptions.ConnectionError as err:
        print(f"Error Connecting: {err}")
    except requests.exceptions.Timeout as err:
        print(f"Timeout Error: {err}")
    except requests.exceptions.RequestException as err:
        print(f"Error: {err}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        shortcodes_file = sys.argv[1]
        output_folder = "download"

        # Create output folder if it doesn't exist
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        
        # Empty the output folder
        empty_folder(output_folder)

        # Read shortcodes and download files
        with open(shortcodes_file, 'r') as file:
            shortcodes = file.read().splitlines()

        for shortcode in shortcodes:
            download_file(shortcode, output_folder)
    else:
        print("Please provide a path to the text file containing shortcodes as an argument.")
