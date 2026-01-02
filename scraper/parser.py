from scraper.fetacher import fetch_page_content
from urllib.parse import urljoin
import logging
import os

logger = logging.getLogger('scraper')

seen_file = 'scraper/seen_links.txt'

#load already seen links
def load_seen_links():
    if not os.path.exists(seen_file):
        return set()
    with open(seen_file, 'r') as f:
        return set(line.strip() for line in f)
    
#save new link to seen links
def save_seen_link(link):
    with open(seen_file, 'a') as f:
        f.write(link + '\n')

def parse_page(url):
    tree = fetch_page_content(url)
    if tree is None:
        return []
    seen_links = load_seen_links()
    items = []
    try:
        article_nodes = tree.xpath('//article[@class="normal" or @class="photo_story"]')

        for node in article_nodes:
            title = node.xpath('.//h2/a/text()')
            link = node.xpath('.//h2/a/@href')

            if not title or not link:
                continue
            full_link = urljoin(url, link[0].strip())

            #skip already seen links
            if full_link in seen_links:
                continue
            items.append({
                'title': title[0].strip(),
                'link': full_link
            })

            #mark as seen
            save_seen_link(full_link)

        logger.info(f"Parsed {len(items)} new items from {url}")
    except Exception as e:
        print(f"Error parsing the page: {e}")
    return items