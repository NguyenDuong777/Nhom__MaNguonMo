import cv2
import numpy as np
import serial
import time

ser = serial.Serial("COM3", 115200, 8, "N", 1)
cap = cv2.VideoCapture(0)

# Đặt độ phân giải cho Camera.
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
width = int(cap.get(3))
height = int(cap.get(4))

# Khởi tạo biến đảo ngược Camera.
Flip_CAM = False

# Trạng thái ban đầu của các nút bấm và đèn LED
LED_State = np.array([False, False, False, False, False, False], dtype=bool)

# Chọn tọa độ căn lề và khoảng cách của các phím.
start_x = (width // 6 - 100) // 2
range_button = start_x * 2
start_y = 25

# Khởi tạo vị trí các nút
buttons = [(start_x + i * (100 + range_button), start_y, start_x + i * (100 + range_button) + 100, start_y + 100) for i in range(6)]

# Vẽ kích thước nút nhấn với kích thước 100x100
def draw_button(frame, x1, y1, x2, y2, text, status):
    state = ": ON" if status else ": OFF"
    text = text + state

    # Tính kích thước của chữ
    text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)[0]

    # Chiều rộng và chiều cao của hình chữ nhật
    rect_width = x2 - x1
    rect_height = y2 - y1

    # Tính toán vị trí để chữ nằm chính giữa hình chữ nhật
    text_x = x1 + (rect_width - text_size[0]) // 2
    text_y = y1 + (rect_height + text_size[1]) // 2

    # Vẽ hình chữ nhật và chữ lên hình ảnh
    color = (0, 255, 0) if status else (0, 0, 255)
    cv2.rectangle(frame, (x1, y1), (x2, y2), color, -1)
    cv2.putText(frame, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

# Hàm xử lý khi người dùng nhấp chuột
def mouse_click(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        for i, (x1, y1, x2, y2) in enumerate(buttons):
            if x1 <= x <= x2 and y1 <= y <= y2:
                # Đảo trạng thái của LED khi nhấp vào nút
                LED_State[i] = not LED_State[i]
                if LED_State[i]:
                    ser.write(f"{i+1}B".encode())  # Gửi lệnh bật đèn
                else:
                    ser.write(f"{i+1}T".encode())  # Gửi lệnh tắt đèn
                time.sleep(0.1)  # Thêm độ trễ ngắn để tránh việc nhấn nhanh nhiều lần

# Thiết lập sự kiện chuột
cv2.namedWindow("Cua so")
cv2.setMouseCallback("Cua so", mouse_click)

while True:
    ret, frame = cap.read()

    # Nếu nhấn f hoặc F thì đảo ngược Camera.
    if cv2.waitKey(1) == ord("f") or cv2.waitKey(1) == ord("F"):
        Flip_CAM = not Flip_CAM
    if Flip_CAM:
        frame = cv2.flip(frame, 1)

    # Vẽ nút LED1 đến LED6
    for i, (x1, y1, x2, y2) in enumerate(buttons):
        draw_button(frame, x1, y1, x2, y2, f"LED{i + 1}", status=LED_State[i])

    # Hiển thị khung hình
    cv2.imshow("Cua so", frame)

    # Thoát chương trình khi nhấn phím 's'
    if cv2.waitKey(1) == ord("s"):
        break

cap.release()
cv2.destroyAllWindows()
