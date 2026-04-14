import smtplib
import logging
from email.mime.text import MIMEText
from config import ALERT_EMAIL, GMAIL_ADDRESS, GMAIL_APP_PASSWORD

log = logging.getLogger(__name__)

def send_sms(message: str):
    try:
        msg = MIMEText(message)
        msg["Subject"] = "🔔 New Lead Found"
        msg["From"] = GMAIL_ADDRESS
        msg["To"] = ALERT_EMAIL

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
            server.sendmail(GMAIL_ADDRESS, ALERT_EMAIL, msg.as_string())

        log.info("Email sent successfully")
    except Exception as e:
        log.error(f"Email send failed: {e}")
