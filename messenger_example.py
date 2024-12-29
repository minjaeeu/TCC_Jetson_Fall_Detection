from config import (
    SMTP_SERVER,
    SMTP_PORT,
    EMAIL_USER,
    EMAIL_PASSWORD,
    EMAIL_RECIPIENTS,
    TELEGRAM_BASE_API_URL,
    TELEGRAM_CHAT_ID,
)
from messenger import Messenger


# Creates an instance of the notification service
messenger = Messenger(
    smtp_server=SMTP_SERVER,
    smtp_port=SMTP_PORT,
    email_user=EMAIL_USER,
    email_password=EMAIL_PASSWORD,
    telegram_base_api_url=TELEGRAM_BASE_API_URL,
)

# # Send the same e-mail for all the recipients inside the EMAIL_RECIPIENTS list
for recipient in EMAIL_RECIPIENTS:
    messenger.send_email(
        recipient_email=recipient,
        subject="Hi this is test v2",
        body="Hello world, this is a test using smtplib & Python",
        image_filename="example_pic.jpeg",
        image_path=".\example_pic.jpeg",
    )

# Send a message + image to a Telegram chat group
messenger.send_telegram_message(
    message="hello world, this is a test",
    image_path=".\example_pic.jpeg",
    chat_id=TELEGRAM_CHAT_ID,
)
