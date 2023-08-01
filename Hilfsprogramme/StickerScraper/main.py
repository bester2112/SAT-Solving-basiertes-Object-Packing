from stickerscraper import StickerScraper

class Main:
    def __init__(self):
        self.base_url = 'https://www.redbubble.com/shop/stickers?page='
        self.download_folder = 'stickers'

    def run(self):
        number_of_pages = 100  # Sie können die Anzahl der Seiten ändern, die Sie durchsuchen möchten
        sticker_scraper = StickerScraper(self.base_url, self.download_folder)
        sticker_scraper.scrape_stickers(number_of_pages)


if __name__ == '__main__':
    main = Main()
    main.run()