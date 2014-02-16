import requests

def get_page(url):
    r = requests.get(url)
    if r.status_code == 200:
        return r.text
    else:
        raise Exception('Oops! The page returned a status code {status}'.format(status=str(r.status_code)))
