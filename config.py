# E-mail configuriton parameters
SMTP_SERVER = 
SMTP_PORT = 
EMAIL_USER = 
EMAIL_PASSWORD = 
EMAIL_RECIPIENTS = []  # list of e-mails that will receive the message

# Telegram configution parameters
TELEGRAM_API_KEY = # telegram API key
TELEGRAM_BASE_API_URL = f"https://api.telegram.org/bot{TELEGRAM_API_KEY}"
TELEGRAM_CHAT_ID =  # chat id for the group where the bot will send the message to

# Jetson Inference configuration parameters
JETSON_CAMERA_INPUT = 
JETSON_CAMERA_ARGS = ["--input-codec=h264", "--input-height=480", "--input-width=640"]
JETSON_DISPLAY_OUTPUT = 
JETSON_POSE_NET_MODEL = 
JETSON_POSE_NET_THRESHOLD = 
KEYPOINTS_THRESHOLD = 
ALERT_TIME_THRESHOLD = 
FRAME_OUTPUT_PATH = "output/fall_image"

# Name of the person who is being supervised
NAME = 
