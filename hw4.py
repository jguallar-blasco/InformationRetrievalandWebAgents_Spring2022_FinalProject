import logging
import re
import sys
from bs4 import BeautifulSoup
from queue import Queue
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
    # TODO: implement
    return []


def get_links(url):
    res = request.urlopen(url)
    return list(parse_links(url, res.read())) 


def get_nonlocal_links(url):
    '''Get a list of links on the page specificed by the url,
    but only keep non-local links and non self-references.
    Return a list of (link, title) pairs, just like get_links()'''

    # TODO: implement
    links = get_links(url)
   
    filtered = []
    return filtered


def crawl(root, wanted_content=[], within_domain=True):
    '''Crawl the url specified by `root`.
    `wanted_content` is a list of content types to crawl
    `within_domain` specifies whether the crawler should limit itself to the domain of `root`
    '''

    queue = Queue()
    queue.put(root)

    visited = []
    extracted = []

    while not queue.empty():
        content_match = 0 

        url = queue.get()
        if within_domain: # If only urls from within the domain should be accepted
             x = re.search('^(?:https?:\/\/)?(?:[^@\n]+@)?(?:www\.)?([^:\/\n?]+)', root)
             if x.search(url):

                try:
                    req = request.urlopen(url)
                    for content in wanted_content: # Run through wanted content
                        if req.headers['Content-Type'] == content: # Determine if content match
                            content_match = 1 

                    if content_match: 
                        html = req.read()

                        visited.append(url)
                        visitlog.debug(url)

                        for ex in extract_information(url, html):
                            extracted.append(ex)
                            extractlog.debug(ex)

                        for link, title in parse_links(url, html):
                            queue.put(link)
                    else:
                        continue

                except Exception as e:
                    print(e, url)
                
             else: 
                next
        else: # If all urls should be accepted
            try:
                for content in wanted_content: # Run through wanted content
                        if req.headers['Content-Type'] == content: # Determine if content match
                            content_match = 1 

                if content_match:
                    req = request.urlopen(url)
                    html = req.read()

                    visited.append(url)
                    visitlog.debug(url)

                    for ex in extract_information(url, html):
                        extracted.append(ex)
                        extractlog.debug(ex)

                    for link, title in parse_links(url, html):
                        queue.put(link)

            except Exception as e:
                print(e, url)
            

    return visited, extracted


def extract_information(address, html):
    '''Extract contact information from html, returning a list of (url, category, content) pairs,
    where category is one of PHONE, ADDRESS, EMAIL'''

    # TODO: implement
    results = []
    for match in re.findall('\d\d\d-\d\d\d-\d\d\d\d', str(html)):
        results.append((address, 'PHONE', match))
    for match in re.findall('([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)', str(html)):
        results.append((address, 'EMAIL', match))
    for match in re.findall('([a-zA-Z]+[,]? [a-zA-Z]+ (?<!\d)\d{5}(?!\d)+)'):
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