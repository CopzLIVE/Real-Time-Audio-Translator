import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog
import sounddevice as sd
import numpy as np
import whisper
from deep_translator import GoogleTranslator
import threading
import tempfile
import scipy.io.wavfile
import time
import logging
import os
import ssl
import certifi

# Use trusted certificate store
os.environ["SSL_CERT_FILE"] = certifi.where()

# Setup logging
logging.basicConfig(filename="errors.log", level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize Whisper model
model = whisper.load_model("base")

# Config
SAMPLERATE = 16000
recording = False

# Main window
root = tk.Tk()
root.title("Real-Time Audio Translator")

# --- Functions ---

def start_translation():
    global recording
    recording = True
    start_button.config(state=tk.DISABLED)
    stop_button.config(state=tk.NORMAL)
    save_button.config(state=tk.DISABLED)
    status_label.config(text="Status: Recording...", foreground="green")
    threading.Thread(target=record_and_translate_loop, daemon=True).start()

def stop_translation():
    global recording
    recording = False
    start_button.config(state=tk.NORMAL)
    stop_button.config(state=tk.DISABLED)
    save_button.config(state=tk.NORMAL)
    status_label.config(text="Status: Idle", foreground="blue")

def save_transcript():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt")
    if file_path:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(output_box.get("1.0", tk.END))

def record_and_translate_loop():
    output_box.insert(tk.END, "🎤 Starting recording...\n")
    output_box.see(tk.END)

    while recording:
        try:
            duration = duration_var.get()
            audio = sd.rec(int(duration * SAMPLERATE), samplerate=SAMPLERATE, channels=1, dtype='float32')
            sd.wait()

            # Convert float32 audio to 16-bit PCM for Whisper
            int_audio = np.int16(audio * 32767)

            with tempfile.NamedTemporaryFile(suffix=".wav") as f:
                scipy.io.wavfile.write(f.name, SAMPLERATE, int_audio)
                try:
                    result = model.transcribe(f.name)
                    text = result["text"].strip()
                except Exception as e:
                    text = ""
                    output_box.insert(tk.END, f"⚠️ Transcription error: {e}\n")
                    logging.error("Transcription error", exc_info=True)
                    output_box.see(tk.END)

            if text:
                source_lang = source_lang_var.get()
                target_lang = lang_var.get()
                try:
                    translator = GoogleTranslator(
                        source=source_lang if source_lang != "auto" else "auto",
                        target=target_lang
                    )
                    translated = translator.translate(text)

                    if translated.strip() == text.strip():
                        output_box.insert(tk.END, f"⚠️ Translation might be unchanged or not detected.\n")

                    output_box.insert(tk.END, f"🔊 Original: {text}\n")
                    output_box.insert(tk.END, f"🌍 Translated ({target_lang}): {translated}\n\n")
                    output_box.see(tk.END)
                except Exception as e:
                    output_box.insert(tk.END, f"⚠️ Translation error: {e}\n\n")
                    logging.error("Translation error", exc_info=True)
                    output_box.see(tk.END)
            else:
                output_box.insert(tk.END, "⏳ No speech detected...\n")
                output_box.see(tk.END)

            time.sleep(0.1)

        except Exception as e:
            output_box.insert(tk.END, f"⚠️ Unexpected error: {e}\n")
            logging.error("Unexpected error", exc_info=True)
            output_box.see(tk.END)

    output_box.insert(tk.END, "⛔ Stopped.\n\n")
    output_box.see(tk.END)

def on_closing():
    global recording
    recording = False
    root.destroy()

# --- GUI Elements ---

# Top frame
top_frame = ttk.Frame(root)
top_frame.pack(padx=10, pady=5)

start_button = ttk.Button(top_frame, text="▶️ Start", command=start_translation)
start_button.grid(row=0, column=0, padx=5)

stop_button = ttk.Button(top_frame, text="⏹️ Stop", command=stop_translation, state=tk.DISABLED)
stop_button.grid(row=0, column=1, padx=5)

save_button = ttk.Button(top_frame, text="💾 Save Transcript", command=save_transcript, state=tk.DISABLED)
save_button.grid(row=0, column=2, padx=5)

# Target Language selection
lang_var = tk.StringVar(value="en")
lang_menu = ttk.Combobox(top_frame, textvariable=lang_var, width=10)
lang_menu['values'] = ['en', 'es', 'fr', 'de', 'it', 'zh-cn', 'ja', 'ar', 'ru', 'th']
lang_menu.grid(row=0, column=3, padx=5)
lang_menu_label = ttk.Label(top_frame, text="Target Lang:")
lang_menu_label.grid(row=0, column=4, padx=(5, 0))

# Source Language selection
source_lang_var = tk.StringVar(value="auto")
source_lang_menu = ttk.Combobox(top_frame, textvariable=source_lang_var, width=10)
source_lang_menu['values'] = ['auto', 'en', 'zh-CN', 'ja', 'es', 'fr', 'de', 'ru', 'th']
source_lang_menu.grid(row=0, column=5, padx=5)
source_lang_label = ttk.Label(top_frame, text="Source Lang:")
source_lang_label.grid(row=0, column=6, padx=(5, 0))

# Duration setting
duration_var = tk.IntVar(value=5)
duration_spin = ttk.Spinbox(top_frame, from_=1, to=30, textvariable=duration_var, width=5)
duration_spin.grid(row=0, column=7, padx=5)
duration_label = ttk.Label(top_frame, text="Duration (s):")
duration_label.grid(row=0, column=8, padx=(5, 0))

# Status label
status_label = ttk.Label(root, text="Status: Idle", foreground="blue")
status_label.pack(pady=(5, 0))

# Output display
output_box = scrolledtext.ScrolledText(root, width=80, height=25, wrap=tk.WORD)
output_box.pack(padx=10, pady=10)

# Handle graceful shutdown
root.protocol("WM_DELETE_WINDOW", on_closing)

# Start GUI loop
root.mainloop()
