import requests
import logging
import json
import os
from config import KEYWORDS

log = logging.getLogger(__name__)
SEEN_FILE = "seen_posts.json"
HEADERS = {"User-Agent": "LeadScanner/1.0"}
SUBREDDITS = ["Spokane", "SpokaneWA", "spokanebusiness"]

class RedditScanner:
    def __init__(self):
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
        for subreddit in SUBREDDITS:
            url = f"https://www.reddit.com/r/{subreddit}/new.json?limit=50"
            try:
                r = requests.get(url, headers=HEADERS, timeout=15)
                if r.status_code != 200:
                    continue
                posts = r.json().get("data", {}).get("children", [])
                for post in posts:
                    data = post.get("data", {})
                    lead = self._parse_post(data, subreddit)
                    if lead and self._is_relevant(lead) and lead["id"] not in self.seen:
                        self.seen.add(lead["id"])
                        new_leads.append(lead)
            except Exception as e:
                log.error(f"Reddit error ({subreddit}): {e}")
        self._save_seen()
        return new_leads

    def _parse_post(self, data, subreddit):
        try:
            return {
                "id": "reddit_" + data.get("id", ""),
                "title": data.get("title", ""),
                "summary": data.get("selftext", "")[:300],
                "url": "https://reddit.com" + data.get("permalink", ""),
                "location": f"r/{subreddit}",
                "source": "Reddit",
            }
        except Exception:
            return None

    def _is_relevant(self, lead):
        text = (lead["title"] + " " + lead["summary"]).lower()
        return any(kw.lower() in text for kw in KEYWORDS)
