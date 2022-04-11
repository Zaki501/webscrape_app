from datetime import datetime
from decimal import Decimal

from price_parser import parse_price
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver

from constants import AMAZON


class PriceHistory:
    """Turn the dataclass + functions into this Class
    so it's easier to look at"""

    def __init__(self, driver: WebDriver, asin: str):
        """Properties to be added to the database
        Items to be sorted by ASIN, not URL!"""
        self.asin: str
        self.title: str
        self.date: str
        self.amount: Decimal
        self.currency: str

        address = f"{AMAZON}{asin}"

        driver.get(address)
        self.asin = asin
        self._set_title(driver)
        self._set_date()
        self._set_price_and_currency(driver)

    # def _set_asin(self, url: str):
    #     """ Extract asin from url"""
    #     asin = re.search("/[dg]p/([^/]+)", url, flags=re.IGNORECASE)
    #     if asin is None:
    #         raise ValueError("No asin found in Url")
    #     self.asin = asin.group(1)

    def _set_title(self, driver: WebDriver):
        self.title = driver.find_element(By.ID, "productTitle").text

    def _set_date(self):
        self.date = datetime.now().strftime("%Y-%m-%d")

    def _set_price_and_currency(self, driver):
        price_string = driver.find_element(By.CSS_SELECTOR, ".a-price").text
        price = parse_price(price_string)
        self.amount = price.amount_float
        self.currency = price.currency


if __name__ == "__main__":
    pass
