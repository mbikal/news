from scraper.parser import parse_page
from scraper.rss_generator import generate_rss_feed
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger("main")

urls = [
    "https://ekantipur.com/news/"
]

def main():
    all_articles = []

    for url in urls:
        logger.info(f"Scraping: {url}")
        articles = parse_page(url)

        if not articles:
            logger.warning(f"No articles found for {url}")
            continue

        all_articles.extend(articles)

    if not all_articles:
        logger.warning("No articles scraped from any source. RSS not generated.")
        return

    generate_rss_feed(
        items=all_articles,
        feed_title="News Nepali Feed",
        feed_link="https://ekantipur.com/news/",
        feed_description="Latest news articles from ekantipur.com",
        output_file="rss/rss.xml",
    )

if __name__ == "__main__":
    main()
