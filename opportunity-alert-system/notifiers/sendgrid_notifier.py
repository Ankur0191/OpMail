# notifiers/sendgrid_notifier.py
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
FROM_EMAIL = os.getenv("SENDGRID_FROM_EMAIL")

def send_email(subject: str, html_content: str, to_emails: list):
    if SENDGRID_API_KEY is None:
        raise EnvironmentError("SENDGRID_API_KEY not set")
    message = Mail(
        from_email=FROM_EMAIL,
        to_emails=to_emails,
        subject=subject,
        html_content=html_content
    )
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        return response.status_code, response.body, response.headers
    except Exception as e:
        print("SendGrid error:", e)
        raise
