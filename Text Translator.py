import tkinter as tk
from tkinter import ttk
from googletrans import Translator

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

# Function to translate text
def translate_text():
    translator = Translator()

    # Get input text
    text_to_translate = text_input.get("1.0", "end-1c")

    # Get selected target language
    selected_language = lang_combo.get()
    target_language = get_language_code(selected_language)

    # Detect source language
    detected_lang = translator.detect(text_to_translate).lang

    # Perform translation
    translated_text = translator.translate(text_to_translate, src=detected_lang, dest=target_language).text

    # Show output
    output_label.config(text=f"Translated Text: {translated_text}", fg="YELLOW")

# GUI setup
root = tk.Tk()
root.title("Text Translator")
root.geometry("450x350")
root.configure(bg="#e0f7fa")

style = ttk.Style()
style.configure("TButton", font=("Helvetica", 12, "bold"))
style.configure("TLabel", font=("Arial", 12, "bold"))

tk.Label(root, text="Enter Text:", bg="#e0f7fa", font=("Arial", 14, "bold"), fg="#528F20").pack(pady=10)
text_input = tk.Text(root, height=5, width=40, font=("Arial", 12), bg="#ffffff")
text_input.pack(pady=5)

tk.Label(root, text="Select Target Language:", bg="#e0f7fa", font=("Arial", 14, "bold"), fg="#2e991f").pack(pady=10)
lang_combo = ttk.Combobox(root, values=["English", "Urdu", "French", "Spanish", "German", "Hindi"], font=("Arial", 12))
lang_combo.set("English")
lang_combo.pack(pady=5)

ttk.Button(root, text="Translate", command=translate_text).pack(pady=20)

output_label = tk.Label(root, text="", wraplength=300, bg="#e0f7fa", font=("Arial", 12, "italic"), fg="green")
output_label.pack(pady=10)

root.mainloop()
