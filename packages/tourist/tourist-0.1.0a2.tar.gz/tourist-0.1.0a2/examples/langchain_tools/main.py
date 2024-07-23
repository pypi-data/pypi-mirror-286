from bs4 import BeautifulSoup as bs
from tourist.core import TouristScraper


TOURIST_BASE = "http://localhost:8000"
TOURIST_X_SECRET = "supersecret"

tourist_scraper = TouristScraper(TOURIST_BASE, TOURIST_X_SECRET)


def get_text_from_page(url: str) -> str:
    page = tourist_scraper.get_page(url)
    soup = bs(page["source_html"], "html.parser")
    text = soup.get_text()
    return text


def get_chain():
    return


if __name__ == "__main__":
    ...
