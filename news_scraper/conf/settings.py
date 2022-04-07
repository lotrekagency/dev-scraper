import re

CLEANR = re.compile('<.*?>') 
FILENAME_SAVED_ARTICLES = "saved_articles.json"
SCRAPER_CONF_FILE = "conf/scraper_conf.json"
TOKEN_GITHUB=""

try:
    from .local_settings import *
except ImportError:
    pass
