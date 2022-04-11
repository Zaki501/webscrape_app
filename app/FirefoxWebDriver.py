# class for the firefox driverwebdriver
# inputs are proxy ip and port
# to be used with a context manager
import random

from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.webdriver import WebDriver

from constants import PATH_TO_DRIVER


class FireFoxBrowser(WebDriver):
    """Wrapper class for firefox webdriver"""

    def __init__(
        self,
        headless: bool = True,
        random_user_agent: bool = False,
        proxy_ip: str = None,
        proxy_port: int = None,
    ):
        # init service and options
        s = Service(PATH_TO_DRIVER)
        options = Options()
        options.headless = headless
        # random user agent
        if random_user_agent is True:
            self.select_user_agent()
            options.set_preference("general.useragent.override", self.user_agent)
        # manually set proxy
        if proxy_ip is not None and proxy_port is not None:
            print("setting proxy...")
            options.set_preference("network.proxy.type", 1)
            options.set_preference("network.proxy.http", proxy_ip)
            options.set_preference("network.proxy.http_port", proxy_port)
            options.set_preference("network.proxy.ssl", proxy_ip)
            options.set_preference("network.proxy.ssl_port", proxy_port)
            options.set_preference("network.proxy.ftp", proxy_ip)
            options.set_preference("network.proxy.ftp_port", proxy_port)
            options.set_preference("network.proxy.socks", proxy_ip)
            options.set_preference("network.proxy.socks_port", proxy_port)
            options.set_preference("network.http.use-cache", False)

        super(FireFoxBrowser, self).__init__(service=s, options=options)
        # print user agent
        print(options.preferences)

    def select_user_agent(self):
        with open("./misc/user-agents.txt") as f:
            # lines = f.readlines()
            line = f.read().splitlines()
        self.user_agent = random.choice(line)


if __name__ == "__main__":
    # x = FireFoxBrowser(random_user_agent=True)
    # with x:
    #     print(x.user_agent)
    proxy_ip = "162.159.242.97"
    proxy_port = 80
    myProxy = f"{proxy_ip}:{str(proxy_port)}"
    print(myProxy)
    pass
