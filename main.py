import logging
from scraper.scraper import scrape_news
from scraper.rss_generator import generate_rss_feed

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("main")

def main():
    items = scrape_news()

    if not items:
        logger.warning("No articles scraped. Exiting.")
        return

    generate_rss_feed(
        items=items,
        feed_title="My News Feed",
        feed_link="https://mbikal.github.io/news/",
        feed_description="Automatically scraped news feed",
        output_file="rss/feed.xml",
    )

if __name__ == "__main__":
    main()
