# Gesture_3D (3D Model Manipulation via Hand Gestures)

## Overview
This innovative system allows users to manipulate the orientation and scale of a 3D model using hand gestures, aiming to replace traditional input devices like keyboards and mice. Developed using MediaPipe for hand tracking and OpenGL for rendering, the application supports intuitive interactions such as rotation along the x and y axes and zoom adjustments. It proves highly effective under optimal lighting conditions with minimal latency, making it ideal for applications in 3D modeling and virtual educational tools.

## Prerequisites
- **Python Version:** Must be between 3.8 and 3.11 for compatibility with the MediaPipe library.
- **Required Libraries:** Execute the following command to install the necessary libraries:
- **Hardware Requirement:** A webcam connected to your computer is required for hand gesture detection.

## Running the Application
1. **Start Hand Tracking:**
 - Open a terminal window.
 - Navigate to the directory containing `Hand_Tracking.py`.
 - Execute the script:
   ```
   python Hand_Tracking.py
   ```
 - Ensure your hand is visible to the camera. This script will activate your webcam, detect hand gestures, and publish the detected gesture data to manipulate the 3D model.

2. **Start 3D Model Visualization:**
 - Open another terminal window.
 - Navigate to the directory containing `3d.py`.
 - Execute the script:
   ```
   python 3d.py
   ```
 - This script listens for messages from `Hand_Tracking.py` and updates the 3D model's orientation and zoom based on your hand movements.

## User Instructions
- **Change Orientation:**
- **X-axis:** Move your hand left or right to rotate the model along the x-axis.
- **Y-axis:** Move your hand up or down to rotate the model along the y-axis.
- **Zoom:**
- **Zoom Out:** Bring the tips of your thumb and pinky closer together.
- **Zoom In:** Move the tips of your thumb and pinky farther apart.

## Notes
- Make sure both scripts are run from their respective terminal windows. Start `Hand_Tracking.py` first.
- If the 3D model does not respond, check the console for error messages in both scripts. This can help diagnose connectivity issues or bugs in the hand gesture detection.
- Ensure compatibility of the Python and library versions with MediaPipe.
- The application uses the ZeroMQ library for communication between the hand tracking and 3D rendering scripts.
- Optimize hand detection performance by adjusting the lighting and background for the webcam and MediaPipe.

## Contributions
Contributions to this project are welcome! If you have improvements or bug fixes, please feel free to fork the repository and submit a pull request. Your contributions can help make this project even better.

## License
This project is open-sourced under the MIT License. See the LICENSE file for more information.
