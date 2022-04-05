
import os
from utils import *

scraper_conf_data = readFile('scraper_conf.json')  

findArticles(scraper_conf_data['sites_conf'])

createGitHubIssues()