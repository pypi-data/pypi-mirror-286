from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from platformdirs import user_cache_dir
import json

from ._util import CookieUtil, SeleniumUtil
from ._config import Config, logger


def login_to_google(driver: webdriver.Chrome = None, url_requires_login: str = None) -> None:
    """
    Login to Google and save cookies to cache
    :param driver: webdriver.Chrome
    :param url_requires_login: str
    :return: None
    
    Example:
    driver = launch_selenium('/path/where/chromedriver')
    login_to_google(driver)
    driver.quit()
    """
    google_cookie_path = user_cache_dir('login_cache', ensure_exists=True) + '/google-cookies.json'
    
    if driver is None:
        driver = SeleniumUtil.launch_selenuim()
    
    if url_requires_login is None:
        url_requires_login = 'https://accounts.google.com'

    google_cookies = None
    try:
        google_cookies = json.load(open(google_cookie_path))
        logger.info('Loading google cookies')
        CookieUtil.add_all_cookies(driver, google_cookies)
    except:
        logger.warning('google-cookies.json not found')
        pass
        
    driver.get(url_requires_login)
    if driver.current_url.startswith(Config.google_login_url):
        logger.warning('Google AutoLogin failure')
        WebDriverWait(driver, Config.WEBDRV_TIMEOUT).until(EC.url_contains(Config.google_path_when_entering_id))
        if Config.google_id is not None:
            WebDriverWait(driver, Config.WEBDRV_TIMEOUT).until(EC.presence_of_element_located((By.ID, 'identifierId')))
            driver.find_element(By.ID, 'identifierId').send_keys(Config.google_id)

        WebDriverWait(driver, Config.WEBDRV_TIMEOUT).until(EC.url_contains(Config.google_path_when_entering_pwd))
        if Config.google_pwd is not None:
            WebDriverWait(driver, Config.WEBDRV_TIMEOUT).until(EC.presence_of_element_located((By.NAME, 'Passwd')))
            driver.find_element(By.NAME, 'Passwd').send_keys(Config.google_pwd)
        WebDriverWait(driver, Config.WEBDRV_TIMEOUT).until(EC.url_contains(url_requires_login.split('/')[2]))
        WebDriverWait(driver, Config.WEBDRV_TIMEOUT).until(lambda _: len(
            list(
                filter(
                    lambda x: x['name'] == 'SID',
                    CookieUtil.get_cookies_for_domain(driver, Config.google_url_for_crawling_cookies)
                    )
                )
            ) > 0)
        logger.info('Assumed google login success')

    google_cookies = CookieUtil.make_to_cookies_dict(
        CookieUtil.get_cookies_for_domain(driver, Config.google_url_for_crawling_cookies)
    )
    
    open(google_cookie_path, 'w').write(json.dumps(google_cookies))
    logger.info('Captured google cookies')
