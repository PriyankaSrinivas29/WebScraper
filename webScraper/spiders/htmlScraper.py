import scrapy
from bs4 import BeautifulSoup
from urllib.parse import urlparse

class HomeSpider(scrapy.Spider):
    name = "htmlScraper"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Referer': 'https://www.google.com/'
    }

    start_urls = [
        "https://www.fiercepharma.com/",
        "https://www.worldpharmanews.com/",
        "https://pharmatimes.com/news/",
        "https://www.worldpharmaceuticals.net/news/",
        "https://health.economictimes.indiatimes.com/news/pharma",
        "https://pmlive.com/",
        "https://firstwordpharma.com/",
        "https://www.techtarget.com/pharmalifesciences"
    ]

    def start_requests(self):
        for url in self.start_urls:
            request = scrapy.Request(url=url, callback=self.parse, headers=self.headers)
            yield request

    def parse(self, response, **kwargs):
        soup = BeautifulSoup(response.text, "html5lib")
        data = soup.find_all('a')
        filename = urlparse(response.url).netloc + ".txt"
        textfile = open("./webScraper/data/htmlLinkFiles/" + filename, 'w')

        try:
            for tag in data:
                href = tag.get('href')
                # Only capture links with news/article pattern in the URL
                if href and ('news' in href or 'article' in href):
                    textfile.write(response.urljoin(str(href)) + "\n")
            textfile.close()
            print("saved")
        except Exception as e:
            print("Error occurred!")
            print(e)
