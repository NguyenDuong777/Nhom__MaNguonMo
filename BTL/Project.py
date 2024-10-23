import cv2
import time

from scipy.special import powm1

import hand as htm
import numpy as np
import math

# ser = serial.Serial("COM6",115200, 8,"N",1)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
detector = htm.handDetector(detectionCon=1)
width = int(cap.get(3))
height = int(cap.get(4))

button_spec = int(input("Nhap kich thuoc phim: "))

# Trạng thái ban đầu của các nút bấm và đèn LED
Switch_state = np.array(
    [[False, False], [False, False], [False, False], [False, False], [False, False], [False, False]], dtype=bool)
LED_State = np.array([False, False, False, False, False, False], dtype=bool)


def distance_between_points(p1, p2):
    """Calculate the Euclidean distance between two points."""
    return math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)


def hand_status(hand_tracking, frame):
    if hand_tracking[12][1] > hand_tracking[11][1] and hand_tracking[16][1] > hand_tracking[15][1] and \
            hand_tracking[20][1] > hand_tracking[19][1] and hand_tracking[8][1] < hand_tracking[9][1]:
        return 1
    else:
        # Vẽ đường thẳng giữa điểm 8 (ngón trỏ) và điểm 4 (ngón cái)
        cv2.line(frame, (hand_tracking[8][0], hand_tracking[8][1]), (hand_tracking[4][0], hand_tracking[4][1]),
                 (127, 255, 212), 3)


def draw_button(frame, x1, y1, x2, y2, text, status):
    state = ": ON" if status else ": OFF"
    text = text + state
    text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)[0]
    rect_width = x2 - x1
    rect_height = y2 - y1
    text_x = x1 + (rect_width - text_size[0]) // 2
    text_y = y1 + (rect_height + text_size[1]) // 2
    color = (0, 255, 0) if status else (0, 0, 255)
    cv2.rectangle(frame, (x1, y1), (x2, y2), color, -1)
    cv2.putText(frame, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)


def tracking(hand_tracking, x1, y1, x2, y2, switch_state, led_state_index):
    x, y = hand_tracking[8][0], hand_tracking[8][1]
    switch_state[0] = switch_state[1]
    if x1 <= x <= x2 and y1 <= y <= y2:
        switch_state[1] = True
    else:
        switch_state[1] = False
    if switch_state[0] and not switch_state[1]:
        time.sleep(0.02)
        LED_State[led_state_index] = not LED_State[led_state_index]


while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    frame = detector.findHands(frame)
    lmlist = detector.findPosition(frame, draw=False)

    start_x = (width // 6 - button_spec) // 2
    range_button = start_x * 2
    start_y = 25

    if lmlist:
        x1,y1 = lmlist[8][0], lmlist[8][1]
        x2,y2 = lmlist[4][0], lmlist[4][1]

        cv2.line(frame, (x1,y1), (x2, y2), (127, 255, 212), 5)
    for i in range(6):
        draw_button(frame, start_x, start_y, start_x + button_spec, start_y + button_spec, f"LED{i + 1}",
                    status=LED_State[i])
        if lmlist:
            tracking(lmlist, start_x, start_y, start_x + button_spec, start_y + button_spec, Switch_state[i], i)
        start_x += (button_spec + range_button)

    cv2.imshow("Cua so", frame)

    if cv2.waitKey(1) == ord("s"):
        break

cap.release()
cv2.destroyAllWindows()
