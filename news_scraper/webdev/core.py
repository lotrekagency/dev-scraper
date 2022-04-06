import json
import requests

def startScraping():
    scraper_conf_data = readFile('scraper_conf.json')  
    for a in scraper_conf_data['sites_conf']:
        if "webdev" in a.keys():
            conf = a
            break
    findArticles(conf['webdev'])

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

def findArticles(conf):
    print(conf)