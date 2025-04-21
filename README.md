# 🤖 Magnus – A Smart Virtual Assistant

Magnus is a powerful and intelligent virtual assistant inspired by J.A.R.V.I.S. from the Iron Man universe. Developed as a final-year project, Magnus is designed to assist users with day-to-day desktop operations, gesture-controlled navigation, and real-time object detection using computer vision.

✨ Built with Python, Magnus combines voice assistance, gesture recognition, and YOLO-based object detection into one seamless smart assistant experience.

---

## 🧠 Features

🎙️ **Voice Command Execution**  
Control your desktop applications using natural voice commands.

🖱️ **Gesture Controlled Mouse**  
Use hand gestures to move the mouse and click — powered by OpenCV and MediaPipe.

🎯 **Real-Time Object Detection**  
Detect and track objects live using YOLO (You Only Look Once) algorithm.

📁 **Desktop Automation**  
Open apps, control browser, play music, and more using speech-based interaction.

🛠️ **Modular Codebase**  
Separate modules for virtual assistant logic, gesture control, and object detection.

--- 

## 🔧 Tech Stack

- **Language:** Python
- **Voice Assistant:** pyttsx3, SpeechRecognition
- **Gesture Recognition:** OpenCV, MediaPipe
- **Object Detection:** YOLOv5 (Darknet)
- **GUI / Automation:** pyautogui, os, subprocess

## 📁 Project Structure
```
main/
├── data/                           # Consist of data files for model
├── models/                         # Consist of trained model of both gesture control mouse and object Detection
├── detect_and_track.py             # Object Detection Code File   
├── main3.py                        # Main python file
└── start.gif                       
```
## 🚀 Getting Started

### 🔧 Prerequisites

- Python 3.8+
- Webcam (for gesture & object detection)
- Microphone (for voice commands)
- YOLOv3 weights and config files in `assets/` folder

### 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/Magnus-Virtual-Assistant.git
   cd Magnus-Virtual-Assistant
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the python application:**
   ```bash
   python Main3.py
   ```

---
