# 🖐️ Hand Gesture Controlled Virtual Mouse

A Python-based virtual mouse application using computer vision and hand tracking that allows users to control their mouse pointer using hand gestures. The project utilizes **OpenCV**, **MediaPipe**, and **PyAutoGUI** to detect hand landmarks and map them to mouse actions.

## 🎯 Features

- 🖱️ **Move Cursor** – Move mouse using index finger.
- 👆 **Left Click** – Tap index and middle fingers together.
- ✊ **Drag** – Make a fist to drag items.
- ⬆️ **Scroll Up** – Show all five fingers.
- ⬇️ **Scroll Down** – Show only the thumb.
- 📋 **Copy** – Raise index and ring fingers.
- 📄 **Paste** – Raise middle and ring fingers.
- 🔁 **Switch Tab** – Raise thumb, index, and middle fingers.


## 🧰 Tech Stack

- [OpenCV](https://opencv.org/)
- [MediaPipe](https://google.github.io/mediapipe/)
- [NumPy](https://numpy.org/)
- [PyAutoGUI](https://pyautogui.readthedocs.io/en/latest/)
- [Math](https://docs.python.org/3/library/math.html)
- [Time](https://docs.python.org/3/library/time.html)



| Gesture                   | Description        | Action           |
| ------------------------- | ------------------ | ---------------- |
| ☝️ Index Finger           | Cursor Move        | Mouse movement   |
| ✌️ Index + Middle Finger  | Left Click         | Single click     |
| ✊ Fist                    | Drag               | Hold + move      |
| 🖐️ All Fingers           | Scroll Up          | Page scroll up   |
| 👍 Thumb Only             | Scroll Down        | Page scroll down |
| 🤟 Index + Ring           | Copy (`Ctrl + C`)  | Text/File copy   |
| ✌ Middle + Ring           | Paste (`Ctrl + V`) | Paste content    |
| 🤘 Thumb + Index + Middle | Switch Tab         | Next browser tab |
