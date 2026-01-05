import cv2
import mediapipe as mp
import math
import time

# ================== Utility Functions ==================

def euclidean(p1, p2):
    return math.dist(p1, p2)

def eye_aspect_ratio(eye):
    vertical = euclidean(eye[1], eye[3])
    horizontal = euclidean(eye[0], eye[2])
    return vertical / horizontal

# ================== Morse Dictionary ==================

MORSE_DICT = {
    ".-": "A", "-...": "B", "-.-.": "C",
    "-..": "D", ".": "E", "..-.": "F",
    "--.": "G", "....": "H", "..": "I",
    ".---": "J", "-.-": "K", ".-..": "L",
    "--": "M", "-.": "N", "---": "O",
    ".--.": "P", "--.-": "Q", ".-.": "R",
    "...": "S", "-": "T", "..-": "U",
    "...-": "V", ".--": "W", "-..-": "X",
    "-.--": "Y", "--..": "Z"
}

# ================== MediaPipe ==================

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True
)

# ================== Webcam ==================

cap = cv2.VideoCapture(0)

# ================== Eye Landmarks ==================

LEFT_EYE = [33, 159, 133, 145]
RIGHT_EYE = [362, 386, 263, 374]

# ================== Thresholds ==================

EAR_THRESHOLD = 0.20

DOT_MAX_DURATION = 0.25     # seconds
SHORT_GAP = 0.6             # same letter
MEDIUM_GAP = 1.5            # next letter
LONG_GAP = 2.5              # space

# ================== State ==================

eye_closed = False
close_start_time = None
last_blink_time = None

current_morse = ""
decoded_text = ""

# ================== Main Loop ==================

while True:
    ret, frame = cap.read()
    if not ret:
        break

    h, w, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)

    blink_status = "NO FACE"

    if results.multi_face_landmarks:
        face = results.multi_face_landmarks[0]

        left_eye, right_eye = [], []

        for idx in LEFT_EYE:
            lm = face.landmark[idx]
            left_eye.append((int(lm.x * w), int(lm.y * h)))

        for idx in RIGHT_EYE:
            lm = face.landmark[idx]
            right_eye.append((int(lm.x * w), int(lm.y * h)))

        EAR = (eye_aspect_ratio(left_eye) + eye_aspect_ratio(right_eye)) / 2
        now = time.time()

        # ---------------- Eye Closed ----------------
        if EAR < EAR_THRESHOLD:
            blink_status = "EYE CLOSED"
            if not eye_closed:
                eye_closed = True
                close_start_time = now

        # ---------------- Eye Open ----------------
        else:
            blink_status = "EYE OPEN"
            if eye_closed:
                blink_duration = now - close_start_time
                symbol = "." if blink_duration < DOT_MAX_DURATION else "-"
                current_morse += symbol

                # -------- Gap logic --------
                if last_blink_time is not None:
                    gap = close_start_time - last_blink_time

                    if gap > LONG_GAP:
                        decoded_text += MORSE_DICT.get(current_morse[:-1], "?") + " "
                        print(decoded_text)
                        current_morse = symbol

                    elif gap > MEDIUM_GAP:
                        decoded_text += MORSE_DICT.get(current_morse[:-1], "?")
                        print(decoded_text)
                        current_morse = symbol

                last_blink_time = now
                eye_closed = False

        # ---------------- Draw Eye Points ----------------
        for p in left_eye + right_eye:
            cv2.circle(frame, p, 3, (0, 0, 255), -1)

        # ---------------- Display Overlay ----------------
        cv2.putText(frame, f"EAR: {EAR:.2f}", (30, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        cv2.putText(frame, f"Status: {blink_status}", (30, 75),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)

        cv2.putText(frame, f"Current Morse: {current_morse}", (30, 110),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

        cv2.putText(frame, f"Decoded Text: {decoded_text}", (30, 150),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 200, 255), 2)

    cv2.imshow("Eye Morse Communication System", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
