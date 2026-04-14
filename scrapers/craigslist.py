import requests
import logging
import json
import os
import time
from bs4 import BeautifulSoup
from config import KEYWORDS, CRAIGSLIST_SECTIONS

log = logging.getLogger(__name__)

SEEN_FILE = "seen_posts.json"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}

class CraigslistScanner:
    def __init__(self, location_tuple):
        self.subdomain, self.location = location_tuple
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        self.seen = self._load_seen()

    def _load_seen(self):
        if os.path.exists(SEEN_FILE):
            with open(SEEN_FILE, "r") as f:
                return set(json.load(f))
        return set()

    def _save_seen(self):
        with open(SEEN_FILE, "w") as f:
            json.dump(list(self.seen), f)

    def scan(self):
        new_leads = []
        for section in CRAIGSLIST_SECTIONS:
            url = f"https://{self.subdomain}.craigslist.org/search/{section}"
            log.info(f"Scanning: {url}")
            try:
                r = self.session.get(url, timeout=15)
                if r.status_code != 200:
                    log.warning(f"Got {r.status_code} for {url}")
                    continue

                soup = BeautifulSoup(r.content, "html.parser")
                listings = soup.select("li.cl-static-search-result")

                for item in listings:
                    lead = self._parse_listing(item, section)
                    if lead and self._is_relevant(lead) and lead["id"] not in self.seen:
                        self.seen.add(lead["id"])
                        new_leads.append(lead)

                time.sleep(0.5)

            except Exception as e:
                log.error(f"Error scanning {url}: {e}")

        self._save_seen()
        return new_leads

    def _parse_listing(self, item, section):
        try:
            link_tag = item.select_one("a")
            title_tag = None  # unused
            price_tag = item.select_one(".priceinfo")
            location_tag = item.select_one(".location")

            post_url = link_tag["href"] if link_tag else ""
            post_id = item.get("data-pid", post_url)
            title = item.get("title", item.select_one(".title").get_text(strip=True) if item.select_one(".title") else "No title")
            price = price_tag.get_text(strip=True) if price_tag else ""
            area = location_tag.get_text(strip=True) if location_tag else self.location

            return {
                "id":       post_id,
                "title":    title,
                "url":      post_url,
                "price":    price,
                "location": area,
                "section":  section,
                "source":   "Craigslist",
            }
        except Exception as e:
            log.debug(f"Parse error: {e}")
            return None

    def _is_relevant(self, lead):
        text = lead["title"].lower()
        return any(kw.lower() in text for kw in KEYWORDS)
