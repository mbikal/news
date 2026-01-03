from feedgenerator import Rss201rev2Feed
import logging
import os

logger = logging.getLogger('scraper')

SEEN_FILE = "rss/seen_links.txt"


def load_seen_links():
    if not os.path.exists(SEEN_FILE):
        return set()
    with open(SEEN_FILE, "r") as f:
        return set(line.strip() for line in f)


def save_seen_links(links):
    with open(SEEN_FILE, "a") as f:
        for link in links:
            f.write(link + "\n")


def generate_rss_feed(items, feed_title, feed_link, feed_description, output_file):
    seen_links = load_seen_links()
    new_items = []

    # Filter only NEW articles
    for article in items:
        link = article.get("link")
        if link and link not in seen_links:
            new_items.append(article)

    # 🚫 NO new items → DO NOTHING
    if not new_items:
        logger.info("No new articles found. RSS feed not updated.")
        return

    feed = Rss201rev2Feed(
        title=feed_title,
        link=feed_link,
        description=feed_description,
        language="en",
    )

    for article in new_items:
        feed.add_item(
            title=article.get("title", "No Title"),
            link=article.get("link", ""),
            description=article.get("description", article.get("title", "")),
            pubdate=article.get("pubdate"),
        )

    try:
        with open(output_file, "w", encoding="utf-8") as f:
            feed.write(f, "utf-8")

        save_seen_links([a["link"] for a in new_items])

        logger.info(f"RSS updated with {len(new_items)} new items")

    except Exception as e:
        logger.error(f"Failed to write RSS feed: {e}")


