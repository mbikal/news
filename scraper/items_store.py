import json
import os
import logging

logger = logging.getLogger("scraper")

ITEMS_FILE = "scraper/items.json"


def load_items():
    if not os.path.exists(ITEMS_FILE):
        return []

    if os.path.getsize(ITEMS_FILE) == 0:
        # File exists but is empty
        return []

    try:
        with open(ITEMS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        logger.warning("items.json is corrupted or invalid. Resetting file.")
        return []


def save_items(items):
    os.makedirs(os.path.dirname(ITEMS_FILE), exist_ok=True)
    with open(ITEMS_FILE, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)
