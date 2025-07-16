image classification 
import tkinter as tk
from tkinter import filedialog
import tensorflow as tf
from tensorflow.keras import layers, models
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import os

def load_image(image_path):
    """Load and preprocess a single image from file."""
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"File not found: {image_path}")
    
    img = Image.open(image_path)   # Open the image
    img = img.resize((128, 128))   # Resize to match input shape for the CNN
    img = np.array(img)            # Convert image to array
    img = img / 255.0              # Normalize pixel values
    img = np.expand_dims(img, axis=0)  # Add batch dimension
    return img

def build_model():
    """Build and compile a simple CNN model."""
    model = models.Sequential([
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=(128, 128, 3)),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.Flatten(),
        layers.Dense(64, activation='relu'),
        layers.Dense(10, activation='softmax')  # Output layer for 10 classes
    ])
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model

def predict_image_class(image_path, model):
    """Load the image, make predictions, and display results."""
    try:
        image = load_image(image_path)
    except FileNotFoundError as e:
        print(e)
        return

    # Make a prediction on the loaded image
    predictions = model.predict(image)

    # Print out the predicted probabilities for each class
    print(f"Results for {os.path.basename(image_path)}:")
    for i, prob in enumerate(predictions[0]):
        print(f"Class {i}: {prob * 100:.2f}%")

    # Display the image along with class-wise predictions
    plt.imshow(Image.open(image_path))
    plt.title("Predicted Class Probabilities")
    plt.axis('off')  # Hide axes
    plt.show()

def main():
    # Build or load a pre-trained model
    model = build_model()

    # Optionally, load pre-trained weights here
    # model.load_weights('path_to_pretrained_weights.h5')

    # Create the root window
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Open file dialog
    file_path = filedialog.askopenfilename(
        title="Open an image file",
        initialdir="/",  # Initial directory
        filetypes=(("Image files", "*.jpg *.jpeg *.png"), ("All files", "*.*"))  # File types
    )

    if file_path:
        # Predict class and display results
        predict_image_class(file_path, model)
    else:
        print("No file selected.")

if __name__ == "__main__":
    main()