from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from selenium import webdriver
from urllib import parse

from ._config import Config, logger

no_chrome_driver_manager = False
try:
    from webdriver_manager.chrome import ChromeDriverManager
except ImportError:
    no_chrome_driver_manager = True
    pass

class CookieUtil:
    def set_cookie_for_domain(driver: webdriver.Chrome, domain: str, cookie: dict):
        driver.execute_cdp_cmd('Network.setCookie', {
            'url': f'https://{domain}',
            'name': cookie['name'],
            'value': cookie['value'],
            'domain': domain,
            'path': cookie.get('path', '/'),
            'secure': cookie.get('secure', True),
            'httpOnly': cookie.get('httpOnly', True),
            'sameSite': cookie.get('sameSite', 'None'),
            'expirationDate': cookie.get('expiry')
        })

    def get_cookies_for_domain(driver: webdriver.Chrome, url):
        return driver.execute_cdp_cmd('Network.getCookies', {'urls':[url]})['cookies']
    
    def make_to_cookies_dict(cookies: list[dict]) -> dict:
        cookies_dict = {}
        for cookie in cookies:
            cookies_dict[cookie['name']] = cookie
        return cookies_dict

    def make_to_essential_cookies_dict(essential_cookies: dict, cookies: list[dict]) -> dict:
        for cookie in cookies:
            if cookie['name'] in essential_cookies:
                def normalize(cookie: dict) -> dict:
                    if 'value' in cookie:
                        #percent decoding
                        cookie['value'] = parse.unquote(cookie['value']).strip()
                    return cookie
                essential_cookies[cookie['name']] = normalize(cookie)
        return essential_cookies

    def add_all_cookies(driver: webdriver.Chrome, cookies: dict):
        for cookie in cookies.values():
            if 'domain' in cookie and cookie['domain'].endswith('co.kr'):
                cookie['domain'] = cookie['domain'][:-5] + 'com'
            
            try:
                CookieUtil.set_cookie_for_domain(driver, cookie['domain'], cookie)
            except:
                logger.debug('skip to set cookie ' + cookie['name'])


class SeleniumUtil:
    def launch_selenuim(driver_path: str = None) -> webdriver.Chrome:
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-extensions")
        if Config.default_profile_path is not None:
            chrome_options.add_argument("--user-data-dir=" + Config.default_profile_path)
        if Config.profile_dir is not None:
            chrome_options.add_argument("--profile-directory=" + Config.profile_dir)
        if driver_path is None:
            if no_chrome_driver_manager:
                raise ImportError('driver_path is None and webdriver_manager is not installed. Please install `pip install webdriver-manager`')
            else:
                driver_path = ChromeDriverManager().install()
        service = Service(driver_path)

        driver = webdriver.Chrome(chrome_options, service)
        return driver

# expose as global function
def launch_selenium(driver_path: str = None) -> webdriver.Chrome:
    """
    Launches a selenium webdriver with the specified driver path.
    :param driver_path: str
    :return: webdriver.Chrome

    Example:
    driver = launch_selenium('/path/where/chromedriver')
    driver.quit()
    """
    return SeleniumUtil.launch_selenuim(driver_path)