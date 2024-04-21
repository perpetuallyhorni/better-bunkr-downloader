import subprocess
import pathlib
import sys
import os
import time
import requests
from bs4 import BeautifulSoup
from time import sleep
from tqdm import tqdm
from http.client import IncompleteRead
from concurrent.futures import ThreadPoolExecutor, as_completed

headers = {
    'Referer':
        'https://get.bunkrr.su/',
    'Sec-Ch-Ua':
        'Not A(Brand";v="99", "Brave";v="121", "Chromium";v="121"',
    'Sec-Ch-Ua-Mobile':
        "?0",
   'Sec-Ch-Ua-Platform':
        "Windows",
    "Upgrade-Insecure-Requests":
        '1',
    "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"}

def extract_media_url(link):
    # Extract media name from the thumbnail's 'src' attribute and format from the text content of the first <p> element
    try:
        # Extract the media name and extension from the thumbnail image source
        thumbnail_tag = link.find("img", class_="grid-images_box-img")
        if thumbnail_tag and "src" in thumbnail_tag.attrs:
            thumbnail_src = thumbnail_tag['src']
            thumbnail_name = thumbnail_src.split('/')[-1]
            base_name, thumbnail_ext = os.path.splitext(thumbnail_name)

        # Extract the actual media format from the text content of the first <p> element
        media_info_tag = link.find("div", class_="grid-images_box-txt")
        if media_info_tag:
            media_info_p = media_info_tag.find("p")
            if media_info_p:
                actual_ext = os.path.splitext(media_info_p.get_text(strip=True))[-1]
                return base_name, actual_ext
    except Exception as e:
        print(f'Error while extracting media from link: {e}')
        return None, None
    return None, None

def check_file_exists(url):
    response = requests.head(url, headers=headers, allow_redirects=True)
    return response.status_code == 200

def download_media(server, base_name, actual_ext, download_directory):
    file_name_with_actual_ext = f"{base_name}{actual_ext}"
    full_media_url = f"{server}/{file_name_with_actual_ext}?download=true"
    if check_file_exists(full_media_url):
        return download_media_with_curl(full_media_url, download_directory, file_name_with_actual_ext)
    return False

def download_media_with_curl(media_url, download_directory, media_name):
    save_path = os.path.join(download_directory, media_name)
    if os.path.exists(save_path):
        print(f"Media already downloaded: {save_path}")
        return True

    # Prepare the curl command
    curl_command = ["curl", "-LO", media_url]

    # Change the current working directory to the download directory
    os.chdir(download_directory)

    try:
        # Execute the curl command with output redirected to DEVNULL
        with open(os.devnull, 'wb') as devnull:
            subprocess.run(curl_command, stdout=devnull, stderr=devnull, check=True)
        print(f"Downloaded media: {save_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error during download: {e}")
        if os.path.exists(save_path):
            os.remove(save_path)
            print("Partial download removed")
        return False
    return True

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <webpage_url>")
        sys.exit(1)

    main_url = sys.argv[1]

    servers = [
        "https://taquito.bunkr.ru",
        "https://milkshake.bunkr.ru",
        "https://fries.bunkr.ru",
        "https://burger.bunkr.ru",
        "https://pizza.bunkr.ru",
        "https://meatballs.bunkr.ru",
        "https://kebab.bunkr.ru",
        "https://i-taquito.bunkr.ru",
        "https://i-milkshake.bunkr.ru",
        "https://i-fries.bunkr.ru",
        "https://i-burger.bunkr.ru",
        "https://i-pizza.bunkr.ru",
        "https://i-meatballs.bunkr.ru",
        "https://i-kebab.bunkr.ru"
    ]

    main_response = requests.get(main_url, headers=headers)
    main_soup = BeautifulSoup(main_response.text, "html.parser")

    h1_element = main_soup.find("h1", class_="text-[24px] font-bold text-dark dark:text-white")

    if not h1_element:
        print("Error: Could not find the <h1> element on the webpage.")
        sys.exit(1)

    links = main_soup.find_all("div", class_="grid-images_box rounded-lg dark:bg-gray-200 xl:aspect-w-7 xl:aspect-h-8 p-2.5 border-2 display relative flex text-center")

    if not links:
        print("Error: Could not find any videos on the webpage.")
        sys.exit(1)

    folder_name = h1_element.get_text(strip=True)
    download_directory = os.path.join(os.getcwd(), folder_name)
    os.makedirs(download_directory, exist_ok=True)

    with ThreadPoolExecutor(max_workers=16) as executor:
        # Create a list to hold the futures
        future_to_media = {
            executor.submit(download_media, server, base_name, actual_ext, download_directory): (server, base_name, actual_ext)
            for link in links
            for server in servers
            for base_name, actual_ext in [extract_media_url(link)]
            if base_name and actual_ext
        }

        # Iterate over the completed futures
        for future in as_completed(future_to_media):
            server, base_name, actual_ext = future_to_media[future]
            file_name_with_actual_ext = f"{base_name}{actual_ext}"
            try:
                success = future.result()
                if success:
                    print(f"Successfully downloaded {file_name_with_actual_ext} from {server}")
                    # Break out of the loop for this media since it's been downloaded
                    break
            except Exception as exc:
                print(f"{file_name_with_actual_ext} generated an exception: {exc}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit(0)