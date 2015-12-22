from bs4 import BeautifulSoup as bs
import requests
import re


def search_query(search_term):

    search_term = 'star wars'
    magnet_links = {}
    values = []
    keys = []
    url = 'https://kat.cr/usearch/'
    search_url = '{0}{1}'.format(url, search_term)
    params = {'sorder': 'desc', 'field': 'seeders'}
    r = requests.get(search_url, params)
    soup = bs(r.text)

    links = soup.find_all(title="Torrent magnet link")

    for link in links:
        values.append(link['href'])

    pattern = r'(.+?)&dn=(.+?)&tr='

    for value in values:
        m = re.match(pattern, value)
        keys.append(' '.join(m.group(2).split('+')))

    magnet_links = dict(zip(keys, values))

    return magnet_links
