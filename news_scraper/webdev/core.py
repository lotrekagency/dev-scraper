import requests
from interface.scraper_interface import ScraperInterface
from bs4 import BeautifulSoup
import re

# as per recommendation from @freylis, compile once only
CLEANR = re.compile('<.*?>') 
FILENAME_SAVED_ARTICLES = "saved_articles.json"
 
class ScraperWebDev(ScraperInterface):
 
    def __init__(self, site_conf):
 
        self.tags = site_conf['tags']
        self.url = site_conf['api_url']
        self.articles_number_each_tag = site_conf['articles_number_each_tag']
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36'
        }
        self.findArticles()
        self.createGitHubIssues()

    def buildApiUrl(self, base_url, tag, extra=None):
        return base_url + tag + extra if extra else base_url + tag

    def findArticles(self):   
        filename = FILENAME_SAVED_ARTICLES
        if len(self.readFile(filename)) <= 0: filename = self.initFile()
        for tag in self.tags:
            try:
                self.r = requests.get(self.buildApiUrl(self.url, tag, '/feed.xml'), headers=self.headers)
                self.status_code = self.r.status_code
            except Exception as e:
                print('Error fetching the URL: ', self.url)
                print(e)
            try:    
                self.soup = BeautifulSoup(self.r.text, 'lxml')
            except Exception as e:
                print('Could not parse the xml: ', self.url)
                print(e)
            self.articles = self.soup.findAll('entry')
            self.articles_dicts = [
                {
                    'title':a.find('title').text,
                    'url':a.find_all('link', href=True)[0]['href'],
                    'description': re.sub(CLEANR, '', a.find('content').text).split('.')[0].replace('\n', ' '),
                    'tag_list' : [tag],
                    'issue_created': 0,
                } for a in self.articles
            ]
            print(self.articles_dicts)
            print(len(self.articles_dicts))
            self.updateFile(self.articles_dicts, self.articles_number_each_tag, FILENAME_SAVED_ARTICLES)
 