import requests
import re
from urlparse import urlparse
from bs4 import BeautifulSoup
from collections import defaultdict


class SavingZelda(object):

    def __init__(self, url, logger):
        self.url = url
        self.logger = logger
        self.body = ""
        self.not_checked = []
        self.list_of_links = []
        self.links_and_status = {}
        self.dead_links = {}
        self.links_by_status = {}

    def get_page(self, url):
        response = requests.get(url, verify=False)
        if response.status_code == 200:
            self.body = response.text
        else:
            message = 'Oops! The page returned a status code {status}'.format(status=str(response.status_code))
            raise Exception(message)

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

    def check_link(self, link):
        self.logger.debug("Checking {0}".format(link))
        try:
            response = requests.get(link, verify=False, allow_redirects=True)
            status = response.status_code
        except requests.exceptions.ConnectionError:
            status = "Nodename nor servname provided, or not known"
        except Exception, e:
            status = str(e)
        self.links_and_status[link] = status

    def check_links(self, list_of_links):
        self.logger.info("Checking links...")
        for link in list_of_links:
            self.check_link(link)

    def is_recursive(self, link):
        base_url_parsed = urlparse(self.url)
        link_parsed = urlparse(link)
        return link_parsed.netloc == base_url_parsed.netloc

    def can_we_save_the_day(self, links_and_status):
        return links_and_status.values().count(200) == len(links_and_status)

    def get_dead_links(self, links_and_status):
        self.dead_links = [link for link in links_and_status if links_and_status[link] != 200]

    def group_links_by_status(self, links_and_status):
        self.links_by_status = defaultdict(list)

        for key, value in sorted(links_and_status.iteritems()):
            self.links_by_status[value].append(key)

    def run(self):
        self.get_page(self.url)
        self.get_links(self.body)
        self.check_links(self.list_of_links)
        self.group_links_by_status(self.links_and_status)

        if self.can_we_save_the_day(self.links_and_status):
            success_message = "No dead links! Zelda is safe and Hyrule is in peace! <3"
            self.logger.info(success_message)
        else:
            self.get_dead_links(self.links_and_status)
            dead_link_message = "Oh no! Hyrule is in great danger! Dead link found: {0}".format(self.dead_links)
            self.logger.info(dead_link_message)
        self.logger.debug("Links not checked: {0}".format(self.not_checked))
        self.logger.debug("Result by status: \n{0}".format(self.links_by_status))


if __name__ == "__main__":
    import sys
    saving_zelda = SavingZelda(sys.argv[1])
    saving_zelda.run()
