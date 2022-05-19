# test the browser and webscraper
# browser -
# webscraper - go to amazon item, grab Pricehistory

import datetime

import pytest

from app.FirefoxWebDriver import FireFoxBrowser
from app.main import extract_asin, track_item
from app.PriceHistory import PriceHistory

# @pytest.mark.app
# def test_browser():
#     """Go to a static website, grab title"""
#     driver = FireFoxBrowser()
#     with driver:
#         driver.get("http://info.cern.ch")
#         print(driver.title)
#         assert driver.title == "http://info.cern.ch"


@pytest.mark.app
def test_pricehistory():
    """Enter an amazon asin, check if it returns an item"""
    item = "https://www.amazon.co.uk/dp/B00006I551/"
    asin = extract_asin(item)
    driver = FireFoxBrowser()
    with driver:
        p_h = track_item(driver, asin)
        print(p_h.__dict__)
        assert isinstance(p_h, PriceHistory) is True
        assert p_h.currency == "£"
        assert 6 < p_h.amount < 20
        assert p_h.title == "CASIO F91W-1 Casual Sport Watch"
        assert p_h.date == datetime.date.today()
