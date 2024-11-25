import smtplib
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
        wpp_api_url: str,
        wpp_api_key: str,
        wpp_phone_number: str,
    ):
        """
        Initializes the NotificationService with SMTP credentials and configurations.

        :param smtp_server: The SMTP server address (e.g., smtp.gmail.com)
        :param smtp_port: The SMTP server port (e.g., 587 for TLS)
        :param email_user: The email address for authentication
        :param email_password: The email password for authentication
        :param api_url: The URL of the WhatsApp API
        :param api_key: The API key for authentication
        :param phone_number: The recipient's phone number (including country code)
        """
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.email_user = email_user
        self.email_password = email_password
        self.wpp_api_url = wpp_api_url
        self.wpp_api_key = wpp_api_key
        self.wpp_phone_number = wpp_phone_number

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
