import zmq
import cv2
import mediapipe as mp
import numpy as np

# Setup ZeroMQ publisher
context = zmq.Context()
publisher = context.socket(zmq.PUB)
publisher.bind("tcp://*:5555")  # Bind publisher to all interfaces on port 5555

# Initialize MediaPipe Hand module.
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, # Dynamic mode (video)
                       max_num_hands=1, # Detect only one hand
                       min_detection_confidence=0.5, # Minimum confidence to detect a hand
                       min_tracking_confidence=0.5) # Minimum confidence to track a hand

# For drawing the hand landmarks on the image.
mp_drawing = mp.solutions.drawing_utils

# Start capturing video from the webcam.
cap = cv2.VideoCapture(0)

# Convert x-coordinate to an angle
def x_to_angle(x):
    m = (500 - 140) / (360 - 0)
    b = 140
    xangle = (x - b) / m
    return xangle

# Convert y-coordinate to an angle
def y_to_angle(y):
    A, B = 50, 390
    c, d = 0, 360
    yangle = (y - A) * (d - c) / (B - A) + c
    return yangle

def distance_to_scale(length, min_length=0, max_length=200):
    # Normalize length to a value between 0 and 10
    return np.interp(length, [min_length, max_length], [0, 10])

while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Ignoring empty camera frame.") # Skip empty frames
        continue

    # Convert color from BGR to RGB for MediaPipe processing
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Process the image to detect and track hands
    results = hands.process(image_rgb)

    # Draw hand landmarks if any are detected
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Extract and calculate the position and angle of the index finger tip
            index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            x = int(index_finger_tip.x * image.shape[1])
            y = int(index_finger_tip.y * image.shape[0])
            xangle = x_to_angle(x)
            yangle = y_to_angle(y)

            # Extract thumb and pinky tip coordinates for distance calculation
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]
            x1, y1 = int(thumb_tip.x * image.shape[1]), int(thumb_tip.y * image.shape[0])
            x2, y2 = int(pinky_tip.x * image.shape[1]), int(pinky_tip.y * image.shape[0])

            # Calculate the distance between thumb and pinky tips and normalize
            length = np.hypot(x2 - x1, y2 - y1)
            scale_value = distance_to_scale(length)

            # Prepare and send a message with the angles and scale value
            message = f"{xangle},{yangle},{scale_value}"
            publisher.send_string(message)

            print(f"Index Finger Tip - X: {x}, Y: {y}, Angle - X: {xangle:.2f}, Y: {yangle:.2f} degrees")  # Print the x, y coordinates and the angle.
            print(f"Zoom value: {scale_value}")
            cv2.circle(image, (x, y), 10, (255, 0, 0), -1)  # Mark the index finger tip with a red circle

    # Display the processed image with hand landmarks
    cv2.imshow('Hand Tracking', image)

    if cv2.waitKey(5) & 0xFF == 27:  # Press 'ESC' to exit.
        break

# Cleanup resources
hands.close()
cap.release()
cv2.destroyAllWindows()
publisher.close()
context.term()

