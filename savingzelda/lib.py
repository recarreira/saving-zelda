import requests
import re
from urlparse import urlparse
from bs4 import BeautifulSoup


class SavingZelda(object):


    def __init__(self, url):
        self.url = url
        self.body = ""
        self.not_checked = []
        self.too_many_redirects = []
        self.list_of_links = []
        self.links_and_status = {}
        self.dead_links = {}


    def get_page(self, url):
        r = requests.get(url, verify=False)
        if r.status_code == 200:
            self.body = r.text
        else:
            raise Exception('Oops! The page returned a status code {status}'.format(status=str(r.status_code)))


    def get_links(self, html):
        soup = BeautifulSoup(html)
        http = re.compile("^http*")
        relative = re.compile("^/")

        for link in soup.find_all('a'):
            href = link.get('href')
            if not href:
                continue
            elif http.findall(href):
                self.list_of_links.append(href)
            elif relative.findall(href):
                base_url = urlparse(self.url)
                url = "{0}://{1}{2}".format(base_url.scheme, base_url.netloc, href)
                self.list_of_links.append(url)
            else:
                self.not_checked.append(href)


    def check_links(self, list_of_links):
        for link in list_of_links:
            print "Checking {0}".format(link)
            try:
                response = requests.get(link, verify=False, allow_redirects=True)
                self.links_and_status[link] = response.status_code
            except requests.exceptions.TooManyRedirects:
                self.too_many_redirects.append(link)


    def can_we_save_the_day(self, links_and_status):
        return links_and_status.values().count(200) == len(links_and_status)


    def get_dead_links(self, links_and_status):
        self.dead_links = [link for link in links_and_status if links_and_status[link] != 200]


    def run(self):
        self.get_page(self.url)
        self.get_links(self.body)
        self.check_links(self.list_of_links)

        if self.can_we_save_the_day(self.links_and_status):
            print "No dead links! Zelda is safe and Hyrule is in peace! <3"
            print "Result: {0}".format(self.links_and_status)
        else:
            self.get_dead_links(self.links_and_status)
            print "Oh no! Hyrule is in great danger! Dead link found: {0}".format(self.dead_links)
        if self.too_many_redirects:
            print "But we could not verify some of the links because of too many redirects: {0}".format(self.too_many_redirects)
        print "Links not checked: {0}".format(self.not_checked)


if __name__ == "__main__":
    import sys
    saving_zelda = SavingZelda(sys.argv[1])
    saving_zelda.run()