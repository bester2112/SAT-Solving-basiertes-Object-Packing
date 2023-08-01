import os
import time
import re
import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


class StickerScraper:
    def __init__(self, base_url, download_folder):
        self.base_url = base_url
        self.download_folder = download_folder

    def extract_sticker_data(self, page_url):
        driver = webdriver.Chrome()
        driver.maximize_window()  # Maximiere das Fenster
        driver.get(page_url)

        # Scroll down the page
        body = driver.find_element(By.TAG_NAME, "body")
        for _ in range(25):
            body.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.5)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()

        sticker_data = []
        for img in soup.find_all('img', {'class': re.compile(r'styles__productImage--\w+')}):
            sticker_url = img.get('src')
            sticker_name = img.get('alt').replace(' Sticker', '').replace(' ', '_').replace('/', '_').replace('\\','_').replace('\r\n', '').replace('.', '')
            sticker_name = sticker_name[:50]  # Begrenzen Sie die Länge des Dateinamens auf maximal 50 Zeichen.
            if sticker_url:
                sticker_data.append((sticker_url, sticker_name))

        return sticker_data

    def download_stickers(self, sticker_data, page):
        if not os.path.exists(self.download_folder):
            os.makedirs(self.download_folder)

        image_count = 1
        for sticker_url, sticker_name in sticker_data:
            file_name = f'img_{page}_{image_count}_{sticker_name}.jpg'
            file_path = os.path.join(self.download_folder, file_name)
            urllib.request.urlretrieve(sticker_url, file_path)

            print('.', end='', flush=True)

            image_count += 1

    def scrape_stickers(self, number_of_pages):
        for page in range(1, number_of_pages + 1):
            page_url = self.base_url + str(page)
            sticker_data = self.extract_sticker_data(page_url)
            self.download_stickers(sticker_data, page)
            print(f'\nSeite {page} abgeschlossen')
