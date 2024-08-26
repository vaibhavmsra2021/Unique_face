import cv2
import os
from datetime import datetime
from deepface import DeepFace
from PIL import Image
import shutil
import io
import tkinter as tk
from tkinter import messagebox

# Set up directory paths (using local file structure)
db_folder_path = 'face_recognition'
os.makedirs(db_folder_path, exist_ok=True)

# Initialize user ID based on existing folders
def initialize_next_user_id(db_folder_path):
    existing_folders = [name for name in os.listdir(db_folder_path) if os.path.isdir(os.path.join(db_folder_path, name))]
    user_ids = [int(folder_name.split('_')[1]) for folder_name in existing_folders if folder_name.startswith('user_')]
    if not user_ids:
        return 1  # If no user folders exist, start with user_1
    return max(user_ids) + 1  # Set the next user ID to the max existing ID + 1

next_user_id = initialize_next_user_id(db_folder_path)

# Global variable to track the connected folder
connected_folder = None

# Function to verify if a captured image matches any existing person
def find_matching_person_folder(captured_img_path, threshold=0.3):  # Adjusted threshold
    best_match = None
    min_distance = threshold

    for user_folder in os.listdir(db_folder_path):
        user_folder_path = os.path.join(db_folder_path, user_folder)
        if os.path.isdir(user_folder_path):
            for img_file in os.listdir(user_folder_path):
                img_path = os.path.join(user_folder_path, img_file)
                try:
                    # Perform verification using Facenet512 model
                    result = DeepFace.verify(
                        img1_path=captured_img_path,
                        img2_path=img_path,
                        model_name="Facenet512",
                        enforce_detection=False
                    )
                    if result["verified"] and result["distance"] < min_distance:
                        min_distance = result["distance"]
                        best_match = user_folder_path
                except Exception as e:
                    print(f"Error in verifying {img_path}: {e}")
                    continue
    return best_match

# Function to create a new person folder
def create_new_person_folder():
    global next_user_id
    new_user_folder = os.path.join(db_folder_path, f"user_{next_user_id}")
    os.makedirs(new_user_folder)
    next_user_id += 1
    return new_user_folder

# Function to connect to a folder
def connect_folder(folder_path):
    global connected_folder
    connected_folder = folder_path
    print(f"Connected to folder: {connected_folder}")
    messagebox.showinfo("Connection Status", f"Connected to folder: {connected_folder}")

# Function to disconnect from a folder
def disconnect_folder():
    global connected_folder
    connected_folder = None
    print("Disconnected from folder.")
    messagebox.showinfo("Connection Status", "Disconnected from folder.")

def compress_and_save_image(image_path, output_path, target_size_kb=200):
    image = Image.open(image_path)
    quality = 90  # Adjusted starting quality
    step = 5
    
    while True:
        buffer = io.BytesIO()
        image.save(buffer, format="JPEG", quality=quality)
        size_kb = len(buffer.getvalue()) / 1024
        if size_kb <= target_size_kb or quality <= 10:
            break
        quality -= step  # Reduce quality step by step
    
    with open(output_path, "wb") as f:
        f.write(buffer.getvalue())

# Function to capture image from webcam
def capture_image():
    global connected_folder
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        return

    cap.release()
    cv2.destroyAllWindows()

    # Save the captured image to a temporary path
    captured_img_path = 'temp_captured.jpg'
    cv2.imwrite(captured_img_path, frame)

    # Check if a folder is connected
    if connected_folder:
        person_folder = connected_folder
        print("Connected folder found. Saving directly.")
    else:
        # Find matching person folder or create a new one
        person_folder = find_matching_person_folder(captured_img_path)

        if person_folder is None:
            person_folder = create_new_person_folder()
            print("No match found. Created a new folder.")
        else:
            print("Match found. Saving to existing folder.")
            connect_folder(person_folder)

    # Save the image
    img_name = datetime.now().strftime("%Y%m%d_%H%M%S") + ".jpg"
    shutil.move(captured_img_path, os.path.join(person_folder, img_name))
    print(f"Image saved in {person_folder}")

# Function to capture and save directly to the connected folder
def capture_and_save():
    global connected_folder
    if not connected_folder:
        print("No folder connected. Please verify or create a new person first.")
        messagebox.showwarning("Capture Error", "No folder connected. Please verify or create a new person first.")
        return

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        return

    cap.release()
    cv2.destroyAllWindows()

    # Save directly to the connected folder with compression
    img_name = datetime.now().strftime("%Y%m%d_%H%M%S") + ".jpg"
    temp_img_path = 'temp_capture_save.jpg'
    
    cv2.imwrite(temp_img_path, frame)
    compress_and_save_image(temp_img_path, os.path.join(connected_folder, img_name))
    os.remove(temp_img_path)  # Clean up the temporary image file
    print(f"Image saved in {connected_folder}")

# GUI setup
root = tk.Tk()
root.title("Face Recognition System")

# Capture and Verify button
btn_capture_verify = tk.Button(root, text="Capture & Verify", command=capture_image)
btn_capture_verify.pack(pady=10)

# Capture and Save button
btn_capture_save = tk.Button(root, text="Capture & Save", command=capture_and_save)
btn_capture_save.pack(pady=10)

# Disconnect button
btn_disconnect = tk.Button(root, text="Disconnect", command=disconnect_folder)
btn_disconnect.pack(pady=10)

# Start the GUI event loop
root.mainloop()
