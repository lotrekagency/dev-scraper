# import stuff
import requests

# import modules
from interface.scraper_interface import ScraperInterface
from conf.settings import FILENAME_SAVED_ARTICLES

class ScraperDevTo(ScraperInterface):
 
    def __init__(self, site_conf):
 
        self.tags = site_conf['tags']
        self.url = site_conf['api_url']
        self.articles_number_each_tag = site_conf['articles_number_each_tag']
        self.findArticles()
        self.createGitHubIssues()

    def buildApiUrl(self, tag):
        """Create the endpoint by the site conf

        Parameters:
        tag: (string): articles tag

        Returns:
        string:api url
        """
        return self.url + "?tag=" + tag

    def findArticles(self): 
        """Find beautifull articles, and save them into a json file
        """  
        filename = FILENAME_SAVED_ARTICLES
        if len(self.readFile(filename)) <= 0: filename = self.initFile()
        for tag in self.tags:
            articles = requests.get(self.buildApiUrl(tag)).json()
            self.updateFile(articles, self.articles_number_each_tag, filename)