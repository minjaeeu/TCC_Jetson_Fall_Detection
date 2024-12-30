import jetson_inference
import jetson_utils
import time
import datetime
from config import (
    SMTP_SERVER,
    SMTP_PORT,
    EMAIL_USER,
    EMAIL_PASSWORD,
    EMAIL_RECIPIENTS,
    TELEGRAM_BASE_API_URL,
    TELEGRAM_CHAT_ID,
    JETSON_CAMERA_INPUT,
    JETSON_DISPLAY_OUTPUT,
    JETSON_POSE_NET_MODEL,
    JETSON_POSE_NET_THRESHOLD,
    KEYPOINTS_THRESHOLD,
    ALERT_TIME_THRESHOLD,
    FRAME_OUTPUT_PATH,
    NAME,
)
from messenger import Messenger
from fall_detect import is_person_fallen, is_rectangle_ratio_grt_1

# Camera and video output configuration
camera = jetson_utils.videoSource(JETSON_CAMERA_INPUT)  # Camera
output = jetson_utils.videoOutput(JETSON_DISPLAY_OUTPUT)  # Output display

# Load the PoseNet model
net = jetson_inference.poseNet(
    JETSON_POSE_NET_MODEL, threshold=JETSON_POSE_NET_THRESHOLD
)

# Creates an instance of the notification service
messenger = Messenger(
    smtp_server=SMTP_SERVER,
    smtp_port=SMTP_PORT,
    email_user=EMAIL_USER,
    email_password=EMAIL_PASSWORD,
    telegram_base_api_url=TELEGRAM_BASE_API_URL,
)

lastSaveTime = time.perf_counter()  # time counter

if __name__ == "__main__":
    key = True
    try:
        while output.IsStreaming():
            # Capture a frame from the camera
            frame = camera.Capture()

            # Process the frame to detect poses
            poses = net.Process(frame)

            # Display information about detected poses and check if anyone is fallen
            for pose in poses:
                if is_rectangle_ratio_grt_1(
                    pose=pose, frame=frame
                ) and is_person_fallen(
                    pose=pose, keypoints_threshold=KEYPOINTS_THRESHOLD
                ):
                    print("*****************")
                    print("ALERT: Person potentially fallen!\n")

                    currentTime = time.perf_counter()
                    # sends a new alert after a given time threshold
                    if (currentTime - lastSaveTime) >= ALERT_TIME_THRESHOLD:
                        # Path there the last frame will be saved to
                        fall_time = datetime.datetime.now()
                        last_frame_path = f"{FRAME_OUTPUT_PATH}_{fall_time}.jpg"
                        # Saving last frame into above mentioned path
                        jetson_utils.saveImage(
                            last_frame_path,
                            frame,
                        )
                        # Send the same e-mail for all the recipients inside the EMAIL_RECIPIENTS list
                        for recipient in EMAIL_RECIPIENTS:
                            messenger.send_email(
                                recipient_email=recipient,
                                subject=f"SOCORRO!!! QUEDA DE {NAME.upper()} DETECTADA ÀS {fall_time.strftime('%Y-%m-%d %H:%M:%S')}",
                                body=f"Uma possível queda foi detectada! Por favor, verifique a situação atual de {NAME}.",
                                image_filename=last_frame_path,
                                image_path=last_frame_path,
                            )

                        # Send a message + image to a Telegram chat group
                        messenger.send_telegram_message(
                            message=f"Uma possível queda foi detectada! Por favor, verifique a situação atual de {NAME}.",
                            image_path=last_frame_path,
                            chat_id=TELEGRAM_CHAT_ID,
                        )
                        lastSaveTime = currentTime  # updates time counter
                    break

            # Render the frame with detected poses
            output.Render(frame)

            # Update the window title with FPS
            output.SetStatus("PoseNet | FPS: {:.2f}".format(net.GetNetworkFPS()))

    except KeyboardInterrupt:
        print("\nExiting.....")
