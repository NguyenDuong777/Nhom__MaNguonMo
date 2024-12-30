import cv2
import sys
import time
import hand as htm
import numpy as np
import serial

# Kiểm tra nếu có đủ đối số dòng lệnh (COM port và độ phân giải)
if len(sys.argv) < 3:
    print("Thiếu đối số: cổng COM và độ phân giải")
    sys.exit()

# Lấy cổng COM và độ phân giải từ đối số dòng lệnh
com_port = sys.argv[1]
resolution = sys.argv[2]

ser = serial.Serial(com_port, 115200, 8, "N", 1)

cap = cv2.VideoCapture(0)
detector = htm.handDetector(detectionCon=1)

# Đặt độ phân giải cho Camera
if resolution == "480":
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
elif resolution == "720":
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
elif resolution == "1080":
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
width = int(cap.get(3))
height = int(cap.get(4))

# Khởi tạo biến đảo ngược Camera
Flip_CAM = True

# Trạng thái nút bấm và đèn LED
Switch_state = np.array([[False, False]] * 6, dtype=bool)
LED_State = np.array([False] * 6, dtype=bool)

# Vị trí chuột
mouseX, mouseY = -1, -1

# Lưu giá trị PWM trước đó
last_pwm_value = 0
last_pwm2_value = 0  # PWM2
pwm_value_b = 0
pwm2_value_b = 0

# Xử lý sự kiện chuột
def mouse_event(event, x, y, flags, param):
    global mouseX, mouseY
    if event == cv2.EVENT_LBUTTONDOWN:
        mouseX, mouseY = x, y

# Tạo cửa sổ trước khi gọi setMouseCallback
cv2.namedWindow("Cua so")
cv2.setMouseCallback("Cua so", mouse_event)
cv2.resizeWindow("Cua so", 1280, 720)
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

def tracking(Hand_tracking, x1, y1, x2, y2, switch_state, led_state_index):
    x, y = Hand_tracking[8][1], Hand_tracking[8][2]
    switch_state[0] = switch_state[1]

    if x1 <= x <= x2 and y1 <= y <= y2:
        switch_state[1] = True
    else:
        switch_state[1] = False

    if switch_state[0] and not switch_state[1]:
        time.sleep(0.02)
        LED_State[led_state_index] = not LED_State[led_state_index]
        if LED_State[led_state_index]:
            ser.write(f"{led_state_index+1}B".encode())
        else:
            ser.write(f"{led_state_index+1}T".encode())

def click_button(x1, y1, x2, y2, led_state_index):
    global mouseX, mouseY
    if x1 <= mouseX <= x2 and y1 <= mouseY <= y2:
        time.sleep(0.1)
        LED_State[led_state_index] = not LED_State[led_state_index]
        if LED_State[led_state_index]:
            ser.write(f"{led_state_index+1}B".encode())
        else:
            ser.write(f"{led_state_index+1}T".encode())
        mouseX, mouseY = -1, -1

def calculate_pwm_from_hand(lmlist, pwm_slider_x1, pwm_slider_x2, pwm_slider_y1):
    global last_pwm_value

    if lmlist:
        x_thumb, y_thumb = lmlist[4][1], lmlist[4][2]  # Ngón cái (ID 4)
        x_index, y_index = lmlist[8][1], lmlist[8][2]  # Ngón trỏ (ID 8)

        # Tính khoảng cách giữa ngón cái và ngón trỏ
        distance = np.sqrt((x_index - x_thumb) ** 2 + (y_index - y_thumb) ** 2)

        # Sử dụng tỷ lệ giữa khoảng cách và chiều dài thanh trượt PWM
        slider_length = pwm_slider_x2 - pwm_slider_x1
        pwm_value = int(min(distance / 10, 100))  # Chuyển đổi khoảng cách thành giá trị PWM

        # Kiểm tra xem ngón tay có nằm trong phạm vi thanh trượt không
        if pwm_slider_x1 < x_index < pwm_slider_x2 and pwm_slider_y1 < y_index < pwm_slider_y1 + 20:
            last_pwm_value = int((x_index - pwm_slider_x1) / slider_length * 100)  # Tính tỷ lệ

    return last_pwm_value

def calculate_pwm2_from_hand(lmlist, pwm_slider_x1, pwm_slider_x2, pwm_slider_y1):
    global last_pwm2_value

    if lmlist:
        x_thumb, y_thumb = lmlist[4][1], lmlist[4][2]  # Ngón cái (ID 4)
        x_index, y_index = lmlist[8][1], lmlist[8][2]  # Ngón trỏ (ID 8)

        # Tính khoảng cách giữa ngón cái và ngón trỏ
        distance = np.sqrt((x_index - x_thumb) ** 2 + (y_index - y_thumb) ** 2)

        # Sử dụng tỷ lệ giữa khoảng cách và chiều dài thanh trượt PWM2
        slider_length = pwm_slider_x2 - pwm_slider_x1
        pwm_value = int(min(distance / 10, 100))  # Chuyển đổi khoảng cách thành giá trị PWM

        # Kiểm tra xem ngón tay có nằm trong phạm vi thanh trượt không
        if pwm_slider_x1 < x_index < pwm_slider_x2 and pwm_slider_y1 < y_index < pwm_slider_y1 + 20:
            last_pwm2_value = int((x_index - pwm_slider_x1) / slider_length * 100)  # Tính tỷ lệ

    return last_pwm2_value

while True:
    ret, frame = cap.read()

    if cv2.waitKey(1) == ord("f") or cv2.waitKey(1) == ord("F"):
        Flip_CAM = not Flip_CAM
    if Flip_CAM:
        frame = cv2.flip(frame, 1)

    frame = detector.findHands(frame)
    lmlist = detector.findPosition(frame, draw=False)

    # Vị trí thanh trượt PWM1
    pwm_slider_x1 = 50
    pwm_slider_x2 = 500
    pwm_slider_y1 = 350
    pwm_slider_y2 = pwm_slider_y1 + 20

    # Vẽ thanh trượt PWM1 với màu nhạt hơn
    cv2.rectangle(frame, (pwm_slider_x1, pwm_slider_y1), (pwm_slider_x2, pwm_slider_y2), (220, 220, 220), -1)
    cv2.line(frame, (pwm_slider_x1, pwm_slider_y1), (pwm_slider_x2, pwm_slider_y1), (0, 0, 0), 2)

    # Tính giá trị PWM từ cử chỉ ngón tay cho PWM1
    pwm_value = calculate_pwm_from_hand(lmlist, pwm_slider_x1, pwm_slider_x2, pwm_slider_y1)
    cv2.rectangle(frame, (pwm_slider_x1 + pwm_value * 4, pwm_slider_y1), (pwm_slider_x1 + pwm_value * 4 + 10, pwm_slider_y2), (0, 255, 0), -1)

    # Hiển thị giá trị PWM1
    cv2.putText(frame, f"PWM1: {pwm_value}", (pwm_slider_x1, pwm_slider_y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    # Gửi giá trị PWM tới STM32 cho PWM1
    if(pwm_value != pwm_value_b):
        ser.write(f"P1{pwm_value:03d}".encode())
    pwm_value_b =pwm_value

    # Vị trí thanh trượt PWM2
    pwm_slider_y1_2 = pwm_slider_y2 + 50  # Tạo khoảng cách giữa 2 thanh trượt
    pwm_slider_y2_2 = pwm_slider_y1_2 + 20

    # Vẽ thanh trượt PWM2 với màu nhạt hơn
    cv2.rectangle(frame, (pwm_slider_x1, pwm_slider_y1_2), (pwm_slider_x2, pwm_slider_y2_2), (220, 220, 220), -1)
    cv2.line(frame, (pwm_slider_x1, pwm_slider_y1_2), (pwm_slider_x2, pwm_slider_y1_2), (0, 0, 0), 2)

    # Tính giá trị PWM2 từ cử chỉ ngón tay
    pwm2_value = calculate_pwm2_from_hand(lmlist, pwm_slider_x1, pwm_slider_x2, pwm_slider_y1_2)
    cv2.rectangle(frame, (pwm_slider_x1 + pwm2_value * 4, pwm_slider_y1_2), (pwm_slider_x1 + pwm2_value * 4 + 10, pwm_slider_y2_2), (0, 255, 0), -1)

    # Hiển thị giá trị PWM2
    cv2.putText(frame, f"PWM2: {pwm2_value}", (pwm_slider_x1, pwm_slider_y1_2 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    # Gửi giá trị PWM tới STM32 cho PWM2

    if(pwm2_value != pwm2_value_b):
        ser.write(f"P2{pwm2_value:03d}".encode())
    pwm2_value_b = pwm2_value

    start_x = (width // 6 - 100) // 2
    range_button = start_x * 2
    start_y = 25

    # Vẽ các nút LED
    for i in range(6):
        draw_button(frame, start_x, start_y, start_x + 100, start_y + 100, f"LED{i + 1}", status=LED_State[i])

        if lmlist:
            tracking(lmlist, start_x, start_y, start_x + 100, start_y + 100, Switch_state[i], i)

        click_button(start_x, start_y, start_x + 100, start_y + 100, i)

        start_x += (100 + range_button)

    # Điều chỉnh kích thước khung hình để hiển thị
    frame = cv2.resize(frame, (1280, 720))  # Giữ kích thước cửa sổ hiển thị

    # Hiển thị kết quả
    cv2.imshow("Cua so", frame)

    if cv2.waitKey(1) == ord("s"):
        for i in range(7):
            ser.write(f"{i}T".encode())
            ser.write(f"P{i}000".encode())
        break

cap.release()
cv2.destroyAllWindows()