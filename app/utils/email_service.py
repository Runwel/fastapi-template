import smtplib
from email.mime.text import MIMEText
from app.core.config import settings

def send_email(to: str, subject: str, body: str):
    """Send an email using SMTP."""
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = settings.EMAIL_FROM
    msg["To"] = to

    try:
        with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
            server.sendmail(settings.EMAIL_FROM, to, msg.as_string())
    except Exception as e:
        print(f"Email sending failed: {e}")
