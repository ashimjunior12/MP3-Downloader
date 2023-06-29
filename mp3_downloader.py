# pip install requests
# pip install beautifulsoup4
# pip install selenium

import time
import os
import requests
import warnings
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

warnings.filterwarnings("ignore", category=DeprecationWarning)

def get_download_link(song_name):
    options = Options()
    options.add_argument("--headless")  # Enable headless mode
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options)

    song_base_url = f'https://www.youtube.com/results?search_query={song_name}'
    driver.get(song_base_url)

    content_of_youtube = driver.page_source
    soup = BeautifulSoup(content_of_youtube, 'lxml')
    link = soup.find('a', {'id':'video-title'})
    video_url = f"https://www.youtube.com{link.get('href')}"

    driver.quit()

    driver = webdriver.Chrome(options=options)
    driver.get('https://ytmp3.nu/')

    time.sleep(2)
    url_input = driver.find_element('xpath', '//*[@id="url"]')
    url_input.send_keys(video_url)

    convert_button = driver.find_element('xpath', '/html/body/form/div[2]/input[3]')
    convert_button.click()

    wait = WebDriverWait(driver, 10)
    download_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@id="download"]/a')))
    download_link = download_button.get_attribute('href')

    driver.quit()

    return download_link

song_name = input("Enter the name of the song: ")
download_link = get_download_link(song_name)
response = requests.get(download_link)

os.chdir("/home/ashim/Downloads/songs")      # Specify the path where you want to download the song.
with open(f"{song_name}.mp3", "wb") as file:
    for chunk in response.iter_content():
        file.write(chunk)

print("Audio Successfully downloaded.")
