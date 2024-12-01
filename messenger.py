import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from typing import Optional


class Messenger:
    def __init__(
        self,
        smtp_server: str,
        smtp_port: int,
        email_user: str,
        email_password: str,
        telegram_base_api_url: str,
    ):
        """
        Initializes the NotificationService with SMTP credentials and configurations.

        :param smtp_server: The SMTP server address (e.g., smtp.gmail.com)
        :param smtp_port: The SMTP server port (e.g., 587 for TLS)
        :param email_user: The email address for authentication
        :param email_password: The email password for authentication
        :param telegram_base_api_url: The URL of the base Telegram API (with the token already included)

        """
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.email_user = email_user
        self.email_password = email_password
        self.telegram_base_api_url = telegram_base_api_url

    def send_email(
        self,
        recipient_email: str,
        subject: str,
        body: str,
        image_path: str,
        image_filename: str,
        sender_email: Optional[str] = None,
    ) -> None:
        """
        Sends an email using the provided SMTP server.

        :param recipient_email: The recipient's email address
        :param subject: The subject of the email
        :param body: The body of the email
        :param image_path: Path to the image to be attached
        :param image_filename: Name to be used for the image attachment
        :param sender_email: The sender's email address (optional, defaults to the authenticated email)
        """
        sender_email = sender_email or self.email_user

        # Create the email message
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = recipient_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        try:
            # Reading the image and attaching it to the msg
            with open(image_path, "rb") as img_file:
                # Create a MIMEImage object from the image
                img_attachment = MIMEImage(img_file.read(), name=image_filename)
                # img_attachment.add_header("Content-ID", "<{0}>".format("logo"))
                img_attachment.add_header("Content-ID", "<image1>")
                img_attachment.add_header(
                    "Content-Disposition", "inline", filename=image_filename
                )
                # Attach the image to the email
                msg.attach(img_attachment)

            # Sending the e-mail
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()  # Start a secure connection
                server.login(self.email_user, self.email_password)
                server.sendmail(sender_email, recipient_email, msg.as_string())
            print(f"Email sent successfully to {recipient_email}.")
        except Exception as e:
            print(f"Failed to send email: {e}")

    def send_telegram_message(
        self, message: str, image_path: str, chat_id: str
    ) -> None:
        """
        Sends a message with a photo to a specific Telegram chat using a bot.
        Note: the bot needs to be configured & added to the chat beforehand.

        :param image_path: The path to the photo file.
        :param message: The message caption to send sent along the photo.
        :param chat_id: Chat ID for the group where the bot will send the message to
        """
        url = f"{self.telegram_base_api_url}/sendPhoto"
        print(url)
        try:
            with open(image_path, "rb") as photo:
                files = {"photo": photo}
                payload = {"chat_id": chat_id, "caption": message}
                response = requests.post(url, data=payload, files=files)
                response.raise_for_status()
                return True
        except requests.RequestException as e:
            print(f"Error sending photo: {e}")
            return False
        except FileNotFoundError:
            print(f"Photo not found at: {image_path}")
            return False
