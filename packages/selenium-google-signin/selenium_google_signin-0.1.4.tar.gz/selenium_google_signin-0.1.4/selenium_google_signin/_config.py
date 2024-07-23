
#= Config ===================================================================#

class Config:
    def _initial_config(cls):
        from os import getenv

        cls.WEBDRV_TIMEOUT = 60*60

        # for launching chrome
        cls.default_profile_path = getenv('DEFAULT_PROFILE_PATH')
        cls.profile_dir = getenv('PROFILE_DIR')

        # for signing in to google
        cls.google_login_url = getenv('GOOGLE_LOGIN_URL', "https://accounts.google.com/v3/signin")
        cls.google_path_when_entering_id = getenv('GOOGLE_PATH_WHEN_ENTERING_ID', "/v3/signin/identifier")
        cls.google_id = getenv('GOOGLE_ID')
        cls.google_path_when_entering_pwd = getenv('GOOGLE_PATH_WHEN_ENTERING_PWD', "/v3/signin/challenge/pwd")
        cls.google_pwd = getenv('GOOGLE_PWD')
        cls.google_url_for_crawling_cookies = getenv('GOOGLE_URL_FOR_CRAWLING_COOKIES', "https://accounts.google.com/o/oauth2/v2/auth")

    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._load_dotenv()
            cls._initial_config(cls)
            
            cls._instance = super(Config, cls).__new__(cls, *args, **kwargs)
        return cls._instance
    
    def _load_dotenv():
        try:
            from dotenv import load_dotenv
            load_dotenv()
        except ImportError:
            pass

# initialize config automatically
Config()

#= Logger ========================================================#

try:
    from loguru import logger
except ImportError:
    # make simple logger
    class Logger:
        def debug(self, *args, **kwargs): 
            print('DEBUG:', *args, **kwargs)
        def info(self, *args, **kwargs):
            print('INFO:', *args, **kwargs)
        def warning(self, *args, **kwargs):
            print('WARNING:', *args, **kwargs)
        def error(self, *args, **kwargs):
            print('ERROR:', *args, **kwargs)
    logger = Logger()
