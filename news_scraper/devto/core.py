import json
import requests

FILENAME_SAVED_ARTICLES = "saved_articles.json"

def startScraping():
    scraper_conf_data = readFile('scraper_conf.json')  
    for a in scraper_conf_data['sites_conf']:
        if "devto" in a.keys():
            conf = a
            break
    findArticles(conf['devto'])
    # createGitHubIssues()

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

def writeFile(filename, data):
    with open(filename, "w") as jsonFile:
        json.dump(data, jsonFile, indent = 4)

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
    print(build_url)
    return build_url
    


def initFile():
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


def updateFile(articles, articles_number_each_tag, filename):
    """Add articles for each tag

    Parameters:
    articles (dict): dict of articles for each tag
    articles_number_each_tag (int): max number of artcles for each tag
    filename (string): name of the file

    Returns:
    """
    data = readFile(filename)

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

    writeFile(filename, data)

def findArticles(conf):
    """Find beautifull articles

    Parameters: 
    sites (dict): the configuration for each site to scrape

    Returns: 
    """
    filename = FILENAME_SAVED_ARTICLES
    if len(readFile(filename)) <= 0: filename = initFile()
    for tag in conf['tags']:
        print(tag)
        articles = requests.get(buildApiUrl(conf, tag)).json()
        updateFile(articles, conf['articles_number_each_tag'], filename)

def createGitHubIssues():
    url = "https://api.github.com/repos/lotrekagency/dev-scraper/issues"
    header = {
        "Content-type": "application/json",
        "Accept": "application/vnd.github.v3+json",
        "Authorization" : "token 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"
    } 
    articles = readFile(FILENAME_SAVED_ARTICLES)
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
    writeFile(FILENAME_SAVED_ARTICLES, articles)