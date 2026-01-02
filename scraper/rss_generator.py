from feedgenerator import Rss201rev2Feed
import logging

logger = logging.getLogger('scraper')

def generate_rss_feed(items, feed_title, feed_link, feed_description, output_file):
    feed = Rss201rev2Feed(
        title=feed_title,
        link=feed_link,
        description=feed_description,
        language="en",
    )

    for article in items:
        feed.add_item(
            title=article.get('title', 'No Title'),
            link=article.get('link', ''),
            description=article.get('description', 'No Description'),
            pubdate=article.get('pubdate', None),
        )

    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            feed.write(f, 'utf-8')
        logger.info(f"RSS feed successfully written to {output_file}")
    except Exception as e:
        logger.error(f"Failed to write RSS feed: {e}")