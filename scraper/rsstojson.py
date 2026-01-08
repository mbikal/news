import feedparser
import json

def rss_to_json(rss_url):
    feed = feedparser.parse(rss_url)
    items = []
    
    for entry in feed.entries:
        items.append({
            "title": entry.title,
            "link": entry.link,
            "description": entry.description,
            "published": entry.published
        })
    data = {
        "feed_title": feed.feed.title,
        "items": items
    }
    return data
if __name__ == "__main__":  
    rss_url = "https://raw.githubusercontent.com/mbikal/news/main/rss/rss.xml"
    with open("rss/rss_feed.json", "w", encoding="utf-8") as f:
        json.dump(rss_to_json(rss_url), f, ensure_ascii=False, indent=4)
