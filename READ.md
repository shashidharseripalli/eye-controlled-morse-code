# Eye-Controlled Morse Code Communication System

A real-time eye-based communication system that converts eye blinks into Morse code using computer vision.  
Designed as an assistive Human–Computer Interaction (HCI) project enabling hands-free text input.

---

## 🚀 Features
- Real-time webcam-based eye tracking
- Eye Aspect Ratio (EAR)–based blink detection
- Short blink (`.`) and long blink (`-`) classification
- Time-gap based Morse letter and word segmentation
- Live decoded text display
- Fully real-time, no machine learning training required

---

## 🧠 How It Works

1. Webcam frames are captured using OpenCV
2. Facial landmarks are extracted using MediaPipe FaceMesh
3. Eye Aspect Ratio (EAR) is computed each frame
4. Blink duration determines dot or dash
5. Time gaps between blinks define:
   - Same letter
   - New letter
   - New word
6. Morse sequences are decoded into readable text

---

## 📐 Eye Aspect Ratio (EAR)

\[
EAR = \frac{||p_{upper} - p_{lower}||}{||p_{left} - p_{right}||}
\]

Low EAR values indicate eye closure.

---

## 🛠️ Tech Stack
- Python
- OpenCV
- MediaPipe FaceMesh
- NumPy

---

## ▶️ How to Run

```bash
pip install -r requirements.txt
python src/main.py
