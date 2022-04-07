# import stuff
import json
import requests
import json
from os import walk

# import modules
from conf.settings import FILENAME_SAVED_ARTICLES, TOKEN_GITHUB

class ScraperInterface:

    def buildApiUrl(self):
        pass

    def findArticles(self):
        pass

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

    def writeFile(self, filename, data):
        with open(filename, "w") as jsonFile:
            json.dump(data, jsonFile, indent = 4)

        
    def initFile(self):
        """Initialize the article stored file

        Parameters:

        Returns:
        string:file name
        """
        filename = FILENAME_SAVED_ARTICLES
        with open(filename, "w") as jsonFile:
            data = { 
                "articles" : [] 
            }
            json.dump(data, jsonFile, indent = 4)
        return filename

    def updateFile(self, articles, articles_number_each_tag, filename):
        """Add articles for each tag

        Parameters:
        articles (dict): dict of articles for each tag
        articles_number_each_tag (int): max number of artcles for each tag
        filename (string): name of the file

        Returns:
        """
        data = self.readFile(filename)
        if len(data['articles']) <= 0:
            i = 0 
            for article in articles:
                if i < articles_number_each_tag:
                    data['articles'].append({
                        'title' : article['title'],
                        'description' : article['description'],
                        'url' : article['url'],
                        'tag_list' : article['tag_list'],
                        'issue_created' : 0

                    })
                    i += 1
        else:
            i = 0 
            for article in articles:
                duplicate = False
                for saved in data['articles']:
                    if article['title'] == saved['title']:
                        duplicate = True
                if not duplicate and i < articles_number_each_tag:
                    data['articles'].append({
                        'title' : article['title'],
                        'description' : article['description'],
                        'url' : article['url'],
                        'tag_list' : article['tag_list'],
                        'issue_created' : 0

                    })
                    i += 1

        self.writeFile(filename, data)

    def createGitHubIssues(self):
        url = "https://api.github.com/repos/lotrekagency/dev-scraper/issues"
        header = {
            "Content-type": "application/json",
            "Accept": "application/vnd.github.v3+json",
            "Authorization" : "token " + TOKEN_GITHUB
        } 
        articles = self.readFile(FILENAME_SAVED_ARTICLES)
        for article in articles['articles']:
            if article['issue_created'] == 0:
                arr = [str(r) for r in article['tag_list']]
                body = "## Propose a new article\n\n### "+ article['title'] +"\n\nDescription: "+ article['description'] +"\n\nLink: "+ article['url']+"\n\nTags: " + str(arr)
                payload = {
                    "title": article['title'],
                    "labels" : ["article"],
                    "body" : body
                }
                requests.post(url, data=json.dumps(payload), headers=header)
                article['issue_created'] = 1
        self.writeFile(FILENAME_SAVED_ARTICLES, articles)