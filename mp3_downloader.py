'''
DOCSTRING

STEPS to run the script:
- pip install bs4
- pip install selenium
- pip install requests
- download chromedriver and add it to environment path variables
- other steps
'''


# pip install beautifulsoup4
from bs4 import BeautifulSoup
from time import sleep
from selenium import webdriver                      # pip install selenium
# to enter key strokes and submit button
from selenium.webdriver.common.keys import Keys
import os
import requests
import warnings                       # pip install requests

warnings.filterwarnings("ignore", category=DeprecationWarning)
mp3_website = 'https://ytmp3.nu/'

try:
    def url(song_name):
        song_base_url = f'https://www.youtube.com/results?search_query={song_name}'
        return song_base_url

    search_query = input('Enter the song name: ')

    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    driver = webdriver.Chrome(options=options)
    driver.get(url(search_query))

    def song_url(content):
        soup = BeautifulSoup(content, 'lxml')
        link = soup.find('a', {'id': 'video-title'})
        video_url = f"https://www.youtube.com/{link.get('href')}"
        return video_url

    content_of_youtube = driver.page_source.encode('utf-8').strip()
except:
    pass

try:
    def main(url):
        driver.get(url)
        driver.find_element_by_xpath(
            './/*[@id="url"]').send_keys(song_url(content_of_youtube))
        driver.find_element_by_xpath('.//*[@id="form"]/form/input[3]').click()
        sleep(4)

        content_of_mp3_website = driver.page_source.encode('utf-8').strip()
        sleep(1)
        soup = BeautifulSoup(content_of_mp3_website, 'lxml')
        download_link = soup.find('div', {'id': 'download'})
        song_download = download_link.find('a', href=True)
        content_to_be_download = song_download['href']
        resoponse = requests.get(content_to_be_download)
        driver.quit()
        print('File being downloaded....')

        # Specify the path where you want to download.
        os.chdir('C:\\Users\\User_name\\Downloads')

        with open(f'{search_query}.mp3', 'wb') as file:
            for chunk in resoponse.iter_content():
                file.write(chunk)

        print(f'Successfully downloaded {search_query}.')

    main(mp3_website)


except:
    driver.quit()
    print("Note: Please check your internet connection!!")
