
# 🎧 Real-Time Audio Translator

> A desktop app that listens to live audio, transcribes it using OpenAI's Whisper, and translates it into your chosen language — all in real time.


## 🔥 Features

- 🎙️ Live microphone or system audio input
- 🧠 Offline transcription with OpenAI Whisper
- 🌍 Real-time translation using Deep Translator
- 💬 Supports multiple source and target languages
- 🖥️ Simple GUI built with Tkinter
- 💾 Export transcript to .txt
- ✅ Cross-platform ready (tested on macOS, adaptable for Windows/Linux)


## 🚀 Installation

### 1. Clone the repo

```bash
git clone https://github.com/CopzLIVE/Real-Time-Audio-Translator.git
cd Real-Time-Audio-Translator
```
### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate
# On Windows: venv\Scripts\activate
```
### 3. Install dependencies
```bash
pip install -r requirements.txt
```
### 4. Install FFmpeg
* macOS (Homebrew):
```bash
brew install ffmpeg
```
* Windows: Download from https://ffmpeg.org and add to PATH
* Linux:
```bash
sudo apt install ffmpeg
```
### 5. (macOS only) Set up BlackHole for system audio capture
Instructions: https://github.com/ExistentialAudio/BlackHole
    
## 🧪 Usage

Run the app:
python RealTimeAudioTranslator.py
1. Choose your Target Language (e.g., en, th, ja)
2. (Optional) Select Source Language, or leave as auto
3. Click ▶️ Start
4. Speak or play audio from another source (like YouTube)
5. Watch the live transcription and translation appear
6. Click 💾 Save Transcript to export



## ⚠️ Limitations
* Requires proper audio routing (e.g., BlackHole on macOS)
* Whisper may miss transcription if audio is noisy or too fast
* Some translations may return identical text if the translator fails silently

## 💡 Future Ideas
* Add speech output (text-to-speech)
* Export to subtitle format (SRT)
* Web-based version
* Add speaker diarization or timestamps
## 📄 License
This project uses open-source components and is intended for educational or personal use.Check the license terms for:
* OpenAI Whisper
* Deep Translator


## 🙌 Credits
* Whisper by OpenAI
* Deep Translator
* FFmpeg
* BlackHole Audio Routing