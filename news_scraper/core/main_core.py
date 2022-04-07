# import stuff
import json
from os import walk

# import module
from webdev.core import ScraperWebDev
from devto.core import ScraperDevTo
from conf.settings import SCRAPER_CONF_FILE

class MainCore():

    def __init__(self):
        mypath = "."
        directories = next(walk(mypath), (None, [], None))[1]  # [] if no file

        scraper_conf_data = self.readFile(SCRAPER_CONF_FILE)  
        for scraper_conf in scraper_conf_data['sites_conf']:
            site_name = list(scraper_conf.keys())[0]
            if site_name in directories:
                if site_name == "webdev":
                    ScraperWebDev(scraper_conf[site_name])
                elif site_name == 'devto':
                    ScraperDevTo(scraper_conf[site_name])

    def readFile(self, filename):
        """Read json file 
        
        Parameters:
        filename (string): name of the file

        Returns:
        dict:the content of the file

        """
        f = open(filename) 
        try:
            return json.load(f)
        except ValueError:
            return []
