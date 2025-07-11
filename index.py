import cv2
import numpy as np
import mediapipe as mp
import pyautogui
import time
import math

# Window setup
wCam, hCam = 640, 480
frameR = 100
smoothening = 5
pLocX, pLocY = 0, 0
cLocX, cLocY = 0, 0
screenWidth, screenHeight = pyautogui.size()

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1)
mpDraw = mp.solutions.drawing_utils

prev_action_time = 0

def find_position(img, hand_landmarks):
    lmList = []
    for lm in hand_landmarks.landmark:
        h, w, _ = img.shape
        cx, cy = int(lm.x * w), int(lm.y * h)
        lmList.append((cx, cy))
    return lmList

def fingers_up(lmList):
    fingers = []
    fingers.append(lmList[4][0] < lmList[3][0])  # Thumb
    for tip in [8, 12, 16, 20]:  # Index, Middle, Ring, Pinky
        fingers.append(lmList[tip][1] < lmList[tip - 2][1])
    return fingers

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(imgRGB)

    if result.multi_hand_landmarks:
        for handLms in result.multi_hand_landmarks:
            lmList = find_position(img, handLms)
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

            if len(lmList) >= 21:
                x1, y1 = lmList[8]  # Index fingertip
                fingers = fingers_up(lmList)

                # Cursor Movement (Index only)
                if fingers == [False, True, False, False, False]:
                    x3 = np.interp(x1, (frameR, wCam - frameR), (0, screenWidth))
                    y3 = np.interp(y1, (frameR, hCam - frameR), (0, screenHeight))
                    cLocX = pLocX + (x3 - pLocX) / smoothening
                    cLocY = pLocY + (y3 - pLocY) / smoothening
                    moveX = min(max(cLocX, 1), screenWidth - 1)
                    moveY = min(max(cLocY, 1), screenHeight - 1)
                    pyautogui.moveTo(moveX, moveY)
                    cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
                    pLocX, pLocY = cLocX, cLocY

                # Left Click (Index + Middle)
                elif fingers == [False, True, True, False, False]:
                    length = math.hypot(lmList[8][0] - lmList[12][0], lmList[8][1] - lmList[12][1])
                    if length < 40 and time.time() - prev_action_time > 0.4:
                        pyautogui.click()
                        prev_action_time = time.time()
                        cv2.putText(img, 'Click', (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 3)

                # Drag (Fist)
                elif fingers == [False, False, False, False, False]:
                    dragX = min(max(cLocX, 1), screenWidth - 1)
                    dragY = min(max(cLocY, 1), screenHeight - 1)
                    pyautogui.dragTo(dragX, dragY, duration=0.1)
                    cv2.putText(img, 'Dragging', (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (200, 0, 100), 3)

                # Scroll Up (All fingers)
                elif fingers == [True, True, True, True, True]:
                    pyautogui.scroll(30)
                    cv2.putText(img, 'Scroll Up', (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 200, 0), 3)

                # Scroll Down (Thumb only)
                elif fingers == [True, False, False, False, False]:
                    pyautogui.scroll(-30)
                    cv2.putText(img, 'Scroll Down', (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 200, 0), 3)

                # Copy (Index + Ring)
                elif fingers == [False, True, False, True, False]:
                    if time.time() - prev_action_time > 1:
                        pyautogui.hotkey('ctrl', 'c')
                        prev_action_time = time.time()
                        cv2.putText(img, 'Copied', (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (100, 255, 0), 3)

                # Paste (Middle + Ring)
                elif fingers == [False, False, True, True, False]:
                    if time.time() - prev_action_time > 1:
                        pyautogui.hotkey('ctrl', 'v')
                        prev_action_time = time.time()
                        cv2.putText(img, 'Pasted', (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (100, 255, 0), 3)

                # Switch Tab (Thumb + Index + Middle)
                elif fingers == [True, True, True, False, False]:
                    if time.time() - prev_action_time > 1:
                        pyautogui.hotkey('ctrl', 'tab')
                        prev_action_time = time.time()
                        cv2.putText(img, 'Tab Switched', (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 150, 255), 3)

    # Draw UI frame
    cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 255, 0), 2)
    cv2.imshow("Virtual Mouse - Upgraded", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
