import sqlite3
from dataclasses import dataclass


@dataclass
class ItemData:
    """Data to be returned to user, for confirmation"""

    img_src: str
    title: str
    price: str


@dataclass
class AmazonUrl:
    """Data gathered from scraping amazon item page"""

    string: str
    asin: str
    title: str
    image_src: str
    price: str


class Database(object):
    """SQlite3 Database, only to be used within a context mananger"""

    # DB_LOCATION = DB_PATH

    # check closing the cursor
    # the CRUD methods should open and close a cursor each time,
    # so closing the cursor in __exit__ should be unnecessary

    # def __init__(self, db_location=":memory:"):
    #     print("init")
    #     self.connection = sqlite3.connect(db_location)
    #     self.cur = self.connection.cursor()

    # def __del__(self):
    #     print("del")
    #     self.connection.close()

    def __init__(self, db_location=":memory:"):
        """set up the path"""
        print("init")
        self.path = db_location

    def __enter__(self):
        print(self.path)
        print("enter")

        self.connection = sqlite3.connect(self.path)
        self.cur = self.connection.cursor()
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        print("exit")

        self.cur.close()
        if isinstance(exc_value, Exception):
            self.connection.rollback()
        else:
            self.connection.commit()
        self.connection.close()


if __name__ == "__main__":
    # print("test")
    # s = Service(PATH_TO_DRIVER)
    # options = Options()
    # # options.headless = True
    # firefox_browser = webdriver.Firefox(service=s, options=options)

    # with firefox_browser as browser:
    #     print("in context block")
    #     # browser.__dir__

    # print("end")
    print("/////")
