import requests
from bs4 import BeautifulSoup


class SavingZelda(object):


    def __init__(self, url):
        self.url = url


    def get_page(self, url):
        r = requests.get(url)
        if r.status_code == 200:
            return r.text
        else:
            raise Exception('Oops! The page returned a status code {status}'.format(status=str(r.status_code)))


    def get_links(self, html):
        list_of_links = []
        soup = BeautifulSoup(html)

        for link in soup.find_all('a'):
            list_of_links.append(link.get('href'))
        return list_of_links


    def check_links(self, list_of_links):
        links_and_status = {}
        for link in list_of_links:
            response = requests.get(link)
            links_and_status[link] = response.status_code
        return links_and_status


    def can_we_save_the_day(self, links_and_status):
        alive = True
        for link in links_and_status:
            if links_and_status[link] != 200:
                alive = False
        return alive
