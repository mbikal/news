from feedgenerator import Rss201rev2Feed
import logging
import os
import json
from datetime import datetime

logger = logging.getLogger("scraper")

SEEN_FILE = "rss/items.json"
MAX_ITEMS = 20


def load_items():
    if not os.path.exists(SEEN_FILE):
        return []
    with open(SEEN_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_items(items):
    with open(SEEN_FILE, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)


def generate_rss_feed(items, feed_title, feed_link, feed_description, output_file):
    stored_items = load_items()
    stored_links = {i["link"] for i in stored_items}

    new_items = []
    for article in items:
        if article["link"] not in stored_links:
            new_items.append({
                "title": article["title"],
                "link": article["link"],
                "description": article.get("description", article["title"]),
                "pubdate": datetime.utcnow().isoformat()
            })

    if not new_items:
        logger.info("No new articles found. RSS feed not updated.")
        return

    # Merge + keep newest
    all_items = (new_items + stored_items)[:MAX_ITEMS]
    save_items(all_items)

    feed = Rss201rev2Feed(
        title=feed_title,
        link=feed_link,
        description=feed_description,
        language="en",
    )

    for article in all_items:
        feed.add_item(
            title=article["title"],
            link=article["link"],
            description=article["description"],
            pubdate=datetime.fromisoformat(article["pubdate"]),
            unique_id=article["link"],   # ✅ GUID
        )

    try:
        with open(output_file, "w", encoding="utf-8") as f:
            feed.write(f, "utf-8")
        logger.info(f"RSS updated with {len(new_items)} new items")
    except Exception as e:
        logger.error(f"Failed to write RSS feed: {e}")
