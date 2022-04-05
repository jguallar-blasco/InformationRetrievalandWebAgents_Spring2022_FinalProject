import logging
import re
import sys
from bs4 import BeautifulSoup
from queue import Queue, PriorityQueue
from urllib import parse, request

logging.basicConfig(level=logging.DEBUG, filename='output.log', filemode='w')
visitlog = logging.getLogger('visited')
extractlog = logging.getLogger('extracted')


def parse_links(root, html):
    soup = BeautifulSoup(html, 'html.parser')
    for link in soup.find_all('a'):
        href = link.get('href')
        if href:
            text = link.string
            if not text:
                text = ''
            text = re.sub('\s+', ' ', text).strip()
            yield (parse.urljoin(root, link.get('href')), text)


def parse_links_sorted(root, html):
    soup = BeautifulSoup(html, 'html.parser')
    for link in soup.find_all('a'):
        href = link.get('href')
        if href:
            text = link.string
            if not text:
                text = ''
            text = re.sub('\s+', ' ', text).strip()
            link = parse.urljoin(root, link.get('href'))
            s = parse.urlsplit(link)
            rank = len(s.path) + len(s.query) + len(s.fragment)
            yield (rank, link, text)


def get_links(url):
    res = request.urlopen(url)
    return list(parse_links(url, res.read()))


def get_nonlocal_links(url):
    '''Get a list of links on the page specificed by the url,
    but only keep non-local links and non self-references.
    Return a list of (link, title) pairs, just like get_links()'''

    links = get_links(url)
    domain = parse.urlsplit(url).netloc
    if domain.startswith('www.'):
        domain = domain[4:]
    filtered = []

    for link in links:
        if domain not in link[0]:
            filtered.append(link)

    return filtered


def crawl(root, wanted_content=[], within_domain=True):
    '''Crawl the url specified by `root`.
    `wanted_content` is a list of content types to crawl
    `within_domain` specifies whether the crawler should limit itself to the domain of `root`
    '''

    queue = PriorityQueue()
    queue.put((1, root))

    domain = parse.urlsplit(root).netloc
    if domain.startswith('www.'):
        domain = domain[4:]

    visited = []
    extracted = []

    visited.append(root)

    while not queue.empty():
        rank, url = queue.get()

        # if url in visited:  # need a second check in case two previous pages queue the same page
        #     continue

        if within_domain and domain not in url:
            continue

        try:
            req = request.urlopen(url)
            html = req.read().decode('utf-8')

            if req.headers['Content-Type'] not in wanted_content and wanted_content:
                continue

            # visited.append(url)
            visitlog.debug(url)

            for ex in extract_information(url, html):
                extracted.append(ex)
                extractlog.debug(ex)

            for rank, link, title in parse_links_sorted(url, html):
                if link not in visited:
                    visited.append(link)
                    queue.put((rank + len(title), link))

        except Exception as e:
            print(e, url)

    return visited, extracted


def extract_information(address, html):
    '''Extract contact information from html, returning a list of (url, category, content) pairs,
    where category is one of PHONE, ADDRESS, EMAIL'''

    results = []
    for match in re.findall('\d\d\d-\d\d\d-\d\d\d\d', str(html)):
        results.append((address, 'PHONE', match))
    for match in re.findall('\(\d\d\d\) \d\d\d-\d\d\d\d', str(html)):
        results.append((address, 'PHONE', match))
    for match in re.findall('[\w\.-]+@[a-z0-9\.-]+', str(html)):
        results.append((address, 'EMAIL', match))
    for match in re.findall('((?:[A-Z][a-z]+\s?)+[,])+\s?((?:[A-Z][a-z]*\s?[.]?)+)\s?(\d\d\d\d\d)', str(html)):
        results.append((address, 'ADDRESS', match))
    return results


def writelines(filename, data):
    with open(filename, 'w') as fout:
        for d in data:
            print(d, file=fout)


def main():
    site = sys.argv[1]

    links = get_links(site)
    writelines('links.txt', links)

    nonlocal_links = get_nonlocal_links(site)
    writelines('nonlocal.txt', nonlocal_links)

    visited, extracted = crawl(site)
    writelines('visited.txt', visited)
    writelines('extracted.txt', extracted)


if __name__ == '__main__':
    main()
