import requests

def crawl_html(url):
    responses = requests.get(url)
    return responses.content