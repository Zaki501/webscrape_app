# main functions, to be imported to app
# track item(asin) -> PriceHistory, sent to DB
# regular tracking -> list of asins, for each item,
import re

from constants import AMAZON
from database.create import init_connection
from database.methods import list_of_unique_asins
from FirefoxWebDriver import FireFoxBrowser
from PriceHistory import PriceHistory


def extract_asin(url: str):
    """Extract asin from url"""
    asin = re.search("/[dg]p/([^/]+)", url, flags=re.IGNORECASE)
    if asin is None:
        raise ValueError("No asin found in Url")
    return asin.group(1)


def item_confirmation(url: str) -> str:
    """Return img src, title and price string"""

    ## if confirmed add item with asin to database
    pass


def track_item(browser: FireFoxBrowser, asin: str):
    """Get data for one amazon item"""
    address = f"{AMAZON}{asin}"
    browser.get(address)
    # change pricehistory to take in driver and asin
    return PriceHistory(browser, asin)


def regular_tracking(conn):
    # This will be ran once a day
    # get list of all asins from database
    # for each asin:
    #   open browser, and create pricehistory
    #   close browser
    #   open database
    #   add to database
    #   close
    #   sleep for n seconds

    # error if item isnt availible
    # custon excpetions

    # list of asins will be taken from database

    asins = list_of_unique_asins(conn)

    browser = FireFoxBrowser(headless=False, random_user_agent=True)
    with browser:
        ph_list = []
        for asin in asins:
            print("tracking", asin)
            item = track_item(browser, asin)
            ph_list.append(item.__dict__)

    return ph_list


if __name__ == "__main__":
    # x = "https://www.amazon.co.uk/dp/B07PPTN43Y"
    # browser = FireFoxBrowser(headless=False, random_user_agent=True)
    # with browser:
    #     asin = extract_asin(x)
    #     item = track_item(browser, asin)
    #     print(item.__dict__)
    # pass
    conn = init_connection()

    pass
