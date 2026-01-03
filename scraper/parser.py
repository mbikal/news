from scraper.fetacher import fetch_page_content
from urllib.parse import urljoin
import logging

logger = logging.getLogger("scraper")

def parse_page(url):
    tree = fetch_page_content(url)
    if tree is None:
        return []

    items = []

    try:
        article_nodes = tree.xpath('//article[@class="normal" or @class="photo_story"]')

        for node in article_nodes:
            title = node.xpath('.//h2/a/text()')
            link = node.xpath('.//h2/a/@href')

            if not title or not link:
                continue

            full_link = urljoin(url, link[0].strip())

            items.append({
                "title": title[0].strip(),
                "link": full_link
            })

        logger.info(f"Parsed {len(items)} items from {url}")

    except Exception as e:
        logger.error(f"Error parsing page {url}: {e}")

    return items
