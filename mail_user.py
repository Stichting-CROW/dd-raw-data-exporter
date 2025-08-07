import smtplib
import os
from email.message import EmailMessage

def mail_download_link(email, download_link):
    smtp_server = os.environ.get("SMTP_SERVER", "smtp.example.com")
    smtp_port = int(os.environ.get("SMTP_PORT", 587))
    smtp_user = os.environ.get("SMTP_USER")
    smtp_password = os.environ.get("SMTP_PASSWORD")
    from_email = "info@dashboarddeelmobiliteit.nl"
    from_name = "Dashboard Deelmobiliteit"

    subject = "Export ruwe data Dashboard Deelmobiliteit gereed"

    body = f"""
Beste lezer,

De zojuist door u aangevraagde ruwe data export van het Dashboard Deelmobiliteit staat klaar:

{download_link}

Let op deze link is 24 uur geldig. 

Met vriendelijke groet,

Team Dashboard Deelmobiliteit
"""

    msg = EmailMessage()
    msg["From"] = f"{from_name} <{from_email}>"
    msg["To"] = email
    msg["Subject"] = subject
    msg.set_content(body)

    print("Send mail via SMTP.")
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.send_message(msg)
        print("Send mail result: Success")
    except Exception as e:
        print(f"Send mail result: Failed - {e}")
