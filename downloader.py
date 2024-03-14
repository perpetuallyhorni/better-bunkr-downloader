import sys
import os
import time
import requests
from bs4 import BeautifulSoup
from time import sleep


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


def extract_video_url(link):
    # Extract video name from the 'src' attribute of the 'img' tag
    try:
        video_tag = link.find("img", class_="grid-images_box-img")
        if video_tag and "src" in video_tag.attrs:
            video_name = video_tag['src'].split('thumbs/')[1].split('.png')[0] + ".mp4"
            return video_name
    except Exception as {e}:
        print('Error whille extracting video_urll')
        return None
    return None

def download_video(video_url, download_directory, video_name):
    save_path = os.path.join(download_directory, f"{video_name}.mp4")

    if os.path.exists(save_path):
        print(f"Video already downloaded: {save_path}")
        return True

    response = requests.get(video_url, headers=headers)

    if response.status_code == 404:
        print(f"Error: Video not found (404 Not Found) on server {video_url}")
        return False
    if response.status_code == 429:
        print("Error 429")
        time.sleep(5)
        download_video(video_url=video_url,download_directory=download_directory,video_name=video_name)

    response.raise_for_status()

    with open(save_path, "wb") as video_file:
        video_file.write(response.content)

    print(f"Downloaded video: {save_path}")
    response.close()
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
        "https://pizza.bunkr.ru"
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

    for link in links:
        video_url = extract_video_url(link)
        if video_url:
            for server in servers:
                full_video_url = f"{server}/{video_url}"
                try:
                    if download_video(full_video_url, download_directory, os.path.splitext(os.path.basename(video_url))[0]):
                        sleep(2)
                        break
                except requests.exceptions.RequestException as e:
                    print(f"Error: {e}")
        else:
            print(f"Error: Could not find a valid server for video {video_url} in folder {folder_name}")

if __name__ == "__main__":
    main()