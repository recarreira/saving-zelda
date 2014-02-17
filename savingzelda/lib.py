import requests
from bs4 import BeautifulSoup


def get_page(url):
    r = requests.get(url)
    if r.status_code == 200:
        return r.text
    else:
        raise Exception('Oops! The page returned a status code {status}'.format(status=str(r.status_code)))


def get_links(html):
    list_of_links = []
    soup = BeautifulSoup(html)

    for link in soup.find_all('a'):
        list_of_links.append(link.get('href'))
    return list_of_links
