# 🔔 Lead Scanner

Scans Craigslist for manual labor / service leads and texts you the moment they post.

---

## Setup (5 minutes)

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Get Twilio (free trial works)
1. Sign up at [twilio.com](https://twilio.com)
2. Get a free number (can text to your real number on trial)
3. Grab your Account SID and Auth Token from the dashboard

### 3. Set environment variables
Create a `.env` file or set these in your server environment:
```
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=xxxxxxxxxxxxxxxx
TWILIO_FROM_NUMBER=+15095550000      # your Twilio number
ALERT_TO_NUMBER=+15095551234         # your real phone number
```

Or edit `config.py` directly (less secure, fine for personal use).

### 4. Configure your city and keywords
In `config.py`:
- Change `LOCATIONS` to your city's Craigslist subdomain
- Add/remove keywords as needed

### 5. Run it
```bash
python main.py
```

---

## Hosting 24/7 (Railway — free tier)

1. Push this folder to a GitHub repo
2. Go to [railway.app](https://railway.app) → New Project → Deploy from GitHub
3. Add your environment variables in Railway's Variables tab
4. Deploy — it runs forever

---

## Platform notes

### ✅ Craigslist
Uses RSS feeds — no scraping, clean, reliable.
Best sections:
- `lbg` = Labor Gigs (best)
- `hsg` = Household Services
- `grg` = General Gigs

### ⚠️ Facebook Marketplace
Gated behind login. Phase 2 — requires a dedicated FB account + browser automation (Playwright). Doable but adds complexity.

### ➡️ TaskRabbit & Thumbtack
These are **inbound platforms** — clients search for pros, not the other way around.
**Action:** Create a profile on both. They send YOU leads.
- [TaskRabbit Pro signup](https://www.taskrabbit.com/become-a-tasker)
- [Thumbtack Pro signup](https://www.thumbtack.com/pro)

---

## Selling this to other operators

To set up a new customer:
1. Update `LOCATIONS` with their city
2. Update `ALERT_TO_NUMBER` with their phone
3. Deploy a new Railway instance (free per project)

Monthly cost per customer: ~$0 (Twilio charges ~$0.0079/SMS, negligible volume)

---

## File structure
```
lead_scanner/
├── main.py              # Entry point, main loop
├── config.py            # All settings — edit this
├── notifier.py          # Twilio SMS sender
├── scrapers/
│   ├── __init__.py
│   └── craigslist.py    # Craigslist RSS scanner
├── seen_posts.json      # Auto-generated, tracks already-alerted posts
└── requirements.txt
```
