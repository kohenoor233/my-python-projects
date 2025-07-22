import tkinter as tk
from tkinter import ttk
from gtts import gTTS
import os

# Function to map full name to language code
def get_language_code(full_name):
    language_mapping = {
        "English": "en",
        "Urdu": "ur",
        "French": "fr",
        "Spanish": "es",
        "German": "de",
        "Hindi": "hi"
    }
    return language_mapping.get(full_name, "en")

# Function to convert text to speech
def text_to_speech():
    text = text_input.get("1.0", "end-1c")
    selected_language = lang_combo.get()
    lang_code = get_language_code(selected_language)

    if text.strip():
        speech = gTTS(text=text, lang=lang_code, slow=False)
        speech.save("spoken_output.mp3")
        os.system("start spoken_output.mp3")  # Use 'start' for Windows, 'open' for macOS, or 'xdg-open' for Linux

# GUI setup
root = tk.Tk()
root.title("Text to Speech")
root.geometry("450x300")
root.configure(bg="#fce4ec")  # Light pink background

style = ttk.Style()
style.configure("TButton", font=("Helvetica", 12, "bold"))
style.configure("TLabel", font=("Arial", 12, "bold"))

tk.Label(root, text="Enter Text:", bg="#fce4ec", font=("Arial", 14, "bold"), fg="#880e4f").pack(pady=10)
text_input = tk.Text(root, height=5, width=40, font=("Arial", 12), bg="#ffffff")
text_input.pack(pady=5)

tk.Label(root, text="Select Language for Speech:", bg="#fce4ec", font=("Arial", 14, "bold"), fg="#880e4f").pack(pady=10)
lang_combo = ttk.Combobox(root, values=["English", "Urdu", "French", "Spanish", "German", "Hindi"], font=("Arial", 12))
lang_combo.set("English")
lang_combo.pack(pady=5)

ttk.Button(root, text="Speak", command=text_to_speech).pack(pady=20)

root.mainloop()
