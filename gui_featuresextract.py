
import cv2
import numpy as np
import pandas as pd
from tkinter import Tk, Label, Button, filedialog
from PIL import Image, ImageTk
import os

# Global CSV file where features will be saved
csv_file = 'features.csv'

# Function to extract SIFT features from an image
def extract_sift_features(image_path):
    # Read the image
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    # Initialize SIFT detector
    sift = cv2.SIFT_create()
    # Detect keypoints and descriptors
    keypoints, descriptors = sift.detectAndCompute(img, None)
    
    # Convert keypoints to a more usable format
    keypoints_data = [(kp.pt[0], kp.pt[1], kp.size, kp.angle, kp.response, kp.octave, kp.class_id) for kp in keypoints]
    
    # Print the descriptors to the console
    print("Descriptors Array:")
    print(descriptors)
    
    return keypoints_data, descriptors

# Function to save SIFT features to a single CSV file
def save_features_to_csv(image_name, features, descriptors):
    # Create a DataFrame from the keypoints
    keypoints_df = pd.DataFrame(features, columns=['x', 'y', 'size', 'angle', 'response', 'octave', 'class_id'])
    # Convert descriptors to a DataFrame
    descriptors_df = pd.DataFrame(descriptors)
    
    # Concatenate the keypoints and descriptors
    features_df = pd.concat([keypoints_df, descriptors_df], axis=1)
    
    # Add the image name as a column
    features_df['image_name'] = image_name
    
    # Append the features to the CSV file (without overwriting the previous data)
    if not os.path.exists(csv_file):
        features_df.to_csv(csv_file, index=False)
    else:
        features_df.to_csv(csv_file, mode='a', header=False, index=False)
    
    print(f"Features appended to {csv_file}")

# Function to browse and select an image
def browse_image():
    global img_label, selected_image_path
    # Open file dialog to select image
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
    if file_path:
        selected_image_path = file_path
        
        # Display the selected image on the GUI
        img = Image.open(file_path)
        img.thumbnail((300, 300))  # Resize for display purposes
        img_tk = ImageTk.PhotoImage(img)
        img_label.config(image=img_tk)
        img_label.image = img_tk  # Keep a reference to avoid garbage collection

# Function to handle feature extraction and saving
def extract_and_save_features():
    if selected_image_path:
        # Extract SIFT features
        features, descriptors = extract_sift_features(selected_image_path)
        
        # Save the features to a CSV file
        image_name = os.path.basename(selected_image_path)
        save_features_to_csv(image_name, features, descriptors)

# Create the GUI window
root = Tk()
root.title("SIFT Feature Extractor")

# Initialize the selected_image_path variable
selected_image_path = None

# Create a button to browse for an image
browse_button = Button(root, text="Browse Image", command=browse_image)
browse_button.pack(pady=20)

# Create a button to extract and save features
extract_button = Button(root, text="Extract and Save Features", command=extract_and_save_features)
extract_button.pack(pady=20)

# Create a label to display the selected image
img_label = Label(root)
img_label.pack(pady=20)

# Start the GUI event loop
root.mainloop()
