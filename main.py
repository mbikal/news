from scraper.parser import parse_page
from scraper.rss_generator import generate_rss_feed
from scraper.items_store import load_items, save_items
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

urls = [
    "https://ekantipur.com/news/"
]

# Load previously stored articles
stored_items = load_items()
stored_links = {item["link"] for item in stored_items}

new_items = []

# Scrape
for url in urls:
    scraped_items = parse_page(url)

    for item in scraped_items:
        if item["link"] not in stored_links:
            new_items.append(item)
            stored_items.append(item)

# Save updated items.json ONLY if new items exist
if new_items:
    save_items(stored_items)

    generate_rss_feed(
        items=new_items,   # 👈 only new items go to RSS
        feed_title="News Nepali Feed",
        feed_link="https://ekantipur.com/news/",
        feed_description="Latest news articles from ekantipur.com",
        output_file="rss/rss.xml"
    )
else:
    logging.info("No new articles found. RSS not updated.")
