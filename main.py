import time
import logging
from scrapers.craigslist import CraigslistScanner
from notifier import send_sms
from config import CHECK_INTERVAL_SECONDS, LOCATIONS

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
log = logging.getLogger(__name__)

def run():
    log.info("🚀 Lead Scanner started")
    scanners = [CraigslistScanner(loc) for loc in LOCATIONS]

    while True:
        for scanner in scanners:
            try:
                new_leads = scanner.scan()
                for lead in new_leads:
                    msg = format_lead(lead)
                    log.info(f"New lead found: {lead['title']}")
                    send_sms(msg)
            except Exception as e:
                log.error(f"Scanner error ({scanner.location}): {e}")

        log.info(f"Sleeping {CHECK_INTERVAL_SECONDS}s until next scan...")
        time.sleep(CHECK_INTERVAL_SECONDS)

def format_lead(lead):
    return (
        f"🔔 NEW LEAD [{lead['source']}]\n"
        f"{lead['title']}\n"
        f"📍 {lead.get('location', 'N/A')}\n"
        f"🔗 {lead['url']}"
    )

if __name__ == "__main__":
    run()
