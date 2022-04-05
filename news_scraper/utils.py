import json
import requests

def readFile(filename):
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

def buildApiUrl(conf, tag):
    """Create the endpoint by the site conf

    Parameters:
    conf (dict): the site configuration
    tag: (string): articles tag

    Returns:
    string:api url
    """
    build_url = conf['api_url']
    if conf['latest'] == 'true':
        build_url += "/latest"
    build_url += "?tag=" + tag
    return build_url
    


def initFile():
    """Initialize the article stored file

    Parameters:

    Returns:
    string:file name
    """
    filename = "saved_articles.json"
    with open(filename, "w") as jsonFile:
        data = { 
            "articles" : [] 
        }
        json.dump(data, jsonFile, indent = 4)
    return filename


def updateFile(articles, articles_number_each_tag, filename):
    """Add articles for each tag

    Parameters:
    articles (dict): dict of articles for each tag
    articles_number_each_tag (int): max number of artcles for each tag
    filename (string): name of the file

    Returns:
    """
    data = readFile(filename)
    article_per_tag = 0
    for article in articles:
        if article not in data['articles'] and article_per_tag < articles_number_each_tag:
            data["articles"].append(article)
            article_per_tag += 1

    with open(filename, "w") as jsonFile:
        json.dump(data, jsonFile, indent = 4)

def findArticles(sites):
    """Find beautifull articles

    Parameters: 
    sites (dict): the configuration for each site to scrape

    Returns: 
    """
    filename = initFile()
    for site in sites:
        for tag in site['tags']:
            articles = requests.get(buildApiUrl(site, tag)).json()
            updateFile(articles, site['articles_number_each_tag'], filename)

def createGitHubIssues():
    url = "https://api.github.com/repos/lotrekagency/dev-scraper/issues"
    header = {
        "Content-type": "application/json",
        "Accept": "application/vnd.github.v3+json",
        "Authorization" : "token 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"
    } 
    articles = readFile("saved_articles.json")
    for article in articles['articles']:
        body = "---\nname: New article\nabout: Propose a new article to put in newsletter\ntitle:'["+ article['title'] +"] New article'\nlabels: 'article'\n---\n\n## Propose a new article\n\n### "+ article['title'] +"\n\nDescription: "+ article['description'] +"\n\nLink: "+ article['url']
        payload = {
            "title": article['title'],
            "labels" : ["article"],
            "body" : body
        }
        requests.post(url, data=json.dumps(payload), headers=header )
