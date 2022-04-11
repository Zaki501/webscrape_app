from selenium.webdriver.firefox.webdriver import WebDriver


class ItemData:
    """Data to be returned to user, for confirmation"""

    def __init__(self, driver: WebDriver, url: str):
        self.img_src: str
        self.title: str
        self.price_string: str

        driver.get(url)
        self._set_img_src(driver)
        self._set_title(driver)
        self._set_price_string(driver)

    def _set_img_src(self, driver: WebDriver):
        self.img_src = driver.find_element_by_id("landingImage").get_attribute("src")

    def _set_title(self, driver: WebDriver):
        self.title = driver.find_element_by_id("productTitle").text

    def _set_price_string(self, driver: WebDriver):
        self.price_string = driver.find_element_by_css_selector(".a-price")
