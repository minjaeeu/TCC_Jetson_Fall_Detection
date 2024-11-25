from config import (
    SMTP_SERVER,
    SMTP_PORT,
    EMAIL_USER,
    EMAIL_PASSWORD,
    EMAIL_RECIPIENTS,
    WHATSAPP_API_URL,
    WHATSAPP_API_KEY,
)
from messenger import Messenger


# Creates an instance of the notification service
messenger = Messenger(
    smtp_server=SMTP_SERVER,
    smtp_port=SMTP_PORT,
    email_user=EMAIL_USER,
    email_password=EMAIL_PASSWORD,
    wpp_api_key="teste",
    wpp_api_url="teste",
    wpp_phone_number="teste",
)

# Send the same e-mail for all the recipients inside the EMAIL_RECIPIENTS list
for recipient in EMAIL_RECIPIENTS:
    messenger.send_email(
        recipient_email=recipient,
        subject="Hi this is test v2",
        body="Hello world, this is a test using smtplib & Python",
        image_filename="example_pic.jpeg",
        image_path=".\example_pic.jpeg",
    )
