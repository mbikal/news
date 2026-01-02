from scraper.parser import parse_page
import logging
from  scraper.rss_generator import generate_rss_feed

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
urls = [
    "https://ekantipur.com/news/"
]

all_articles = []
for url in urls:
    articles = parse_page(url)
    all_articles.extend(articles)

generate_rss_feed(
    items=all_articles,
    feed_title="News Nepali Feed",
    feed_link="https://ekantipur.com/news/",
    feed_description="Latest news articles from ekantipur.com",
    output_file="rss/rss.xml"
)