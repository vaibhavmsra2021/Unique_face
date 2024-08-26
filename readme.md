Face Recognition and Verification Script
This Python script provides a simple face recognition and verification system using OpenCV, DeepFace, and a Tkinter-based graphical user interface (GUI). The system captures images from a camera, saves them in a structured directory, and verifies faces against a stored database.

Features
Face Recognition: Detects and recognizes faces from a live camera feed.
Face Verification: Compares a captured face against a database to verify identity.
Image Management: Automatically manages and stores images in a structured folder system.
User Interface: Provides a basic GUI for interaction.
Requirements
Python 3.x
OpenCV (cv2)
DeepFace
Pillow (PIL)
Tkinter (usually comes pre-installed with Python)
Other standard Python libraries (os, shutil, datetime, etc.)
Setup
Install Required Packages: Use the following pip commands to install necessary libraries:

bash
Copy code
pip install opencv-python-headless
pip install deepface
pip install pillow
Directory Structure: The script will create a face_recognition directory in the working directory to store captured images.

Run the Script: Execute the script using Python:

bash
Copy code
python face_V1s.py
Usage
Starting the Program: Upon running the script, the camera feed will open, and the GUI will display options for capturing and verifying images.

Capturing Images: The script saves captured images in a structured folder named face_recognition/user_<ID>, where <ID> is a unique identifier for each user.

Verifying Faces: When a face is captured, the script compares it against the stored images in the face_recognition directory to verify if it matches any existing user.

Image Compression: Images are automatically compressed to be under 200KB before saving to optimize storage usage.

Code Structure
initialize_next_user_id: Initializes the next user ID based on existing folders.
verify_image: Compares a captured image with images in the database for face verification.
capture_image: Captures and saves an image from the camera feed.
Main: Sets up the GUI and integrates all functionalities for user interaction.
Contributing
Feel free to fork this repository and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

License
This project is open-source and available under the MIT License.