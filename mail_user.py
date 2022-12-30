import sendgrid
import os
from sendgrid.helpers.mail import Mail, Email, To, Content, From

def mail_download_link(email, download_link):
    sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email("info@dashboarddeelmobiliteit.nl", "Dashboarddeelmobiliteit")
    to_email = To(email)  # Change to your recipient
    subject = "Export ruwe data dashboarddeelmobiliteit gereed"

    msg = """
Beste lezer,

De zojuist door u aangevraagde ruwe data export van het dashboarddeelmobiliteit staat klaar:

{} 

Let op deze link is 24 uur geldig. 

Met vriendelijke groet,

Team dashboarddeelmobiliteit
    
    
    """.format(download_link)

    content = Content("text/plain", msg)
    mail = Mail(from_email=from_email, to_emails=to_email, subject=subject, plain_text_content=content)

    # Get a JSON-ready representation of the Mail object
    mail_json = mail.get()

    print("Send mail via sendgrid.")
    # Send an HTTP POST request to /mail/send
    response = sg.client.mail.send.post(request_body=mail_json)
    print("Send mail result:")
    print(response.status_code)