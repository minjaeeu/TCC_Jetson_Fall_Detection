import jetson_utils


def is_person_fallen(pose, keypoints_threshold):
    """
    Checks if a person is potentially fallen based on keypoint positions.

    Args:
        pose (jetson_inference.poseNet): A pose object from poseNet containing keypoints and bounding box information.
        keypoints_threshold (int): Threshold to determine abnormal keypoint proximity.

    Returns:
        bool: True if the person is potentially fallen, False otherwise.
    """
    if not pose.Keypoints:
        return False  # If there are no keypoints, no detection is possible

    # Identify keypoints relevant for analysis
    for keypoint in pose.Keypoints:
        if keypoint.ID in [11, 12]:  # Hips
            hip_y = keypoint.y
        elif keypoint.ID in [5, 6]:  # Shoulders
            shoulder_y = keypoint.y
        elif keypoint.ID in [15, 16]:  # Ankles
            ankle_y = keypoint.y

    # Check relative positions of keypoints
    if hip_y and shoulder_y:
        abs_value = abs(hip_y - shoulder_y)
        # Condition: Hips are close to shoulders or ankles (abnormal position)
        print("Hip and shoulder absolute value below threshold:  ", abs_value)
        if abs_value < keypoints_threshold:
            return True  # Conditions met, person is potentially fallen

    if hip_y and ankle_y:
        # Condition: Hips are close to shoulders or ankles (abnormal position)
        abs_value = abs(hip_y - ankle_y)
        print("Hip and ankle absolute value below threshold:  ", abs_value)
        if abs_value < keypoints_threshold:
            return True  # Conditions met, person is potentially fallen

    return False  # If conditions are not met


def is_rectangle_ratio_grt_1(pose, frame):
    """
    Determines if the bounding box around a pose has a width-to-height ratio greater than 1.

    Args:
        pose (jetson_inference.poseNet): A pose object from poseNet containing keypoints and bounding box information.
        frame (jetson_utils.cudaImage): The frame to draw the bounding box on.

    Returns:
        bool: True if the width-to-height ratio is greater than 1, False otherwise.
    """
    # skeleton boundary
    left = int(pose.Left)
    top = int(pose.Top)
    right = int(pose.Right)
    bottom = int(pose.Bottom)

    width = left - right
    height = top - bottom

    # early return in case there is no way to draw the outline box
    if height == 0:
        return False
    else:
        # Draw bounding box
        jetson_utils.cudaDrawRect(
            frame,
            (left, top, right, bottom),
            line_color=(0, 75, 255, 200),
            line_width=3,
        )

    proportion = width / height

    if proportion > 1:
        print("Width to height ration is greater than 1, ratio: ", proportion)
        return True
    else:
        return False
