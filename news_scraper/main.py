import json
from os import walk
from subprocess import call


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

mypath = "."
directories = next(walk(mypath), (None, [], None))[1]  # [] if no file

scraper_conf_data = readFile('scraper_conf.json')  
for scraper_conf in scraper_conf_data['sites_conf']:
    site_name = scraper_conf.keys()[0]
    if site_name in directories:
        site_path = mypath + '/' + site_name
        print(site_name)
        filenames = next(walk(site_path), (None, None, []))[2]  # [] if no file
        if "scraper.py" in filenames:
            site_path += "/scraper.py"
            call(["python", site_path])


            print('script presente')

