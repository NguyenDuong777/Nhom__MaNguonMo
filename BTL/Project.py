import cv2
import time
import hand as htm
import numpy as np
import serial
ser = serial.Serial("COM6",115200, 8,"N",1)


cap = cv2.VideoCapture(0)
detector = htm.handDetector(detectionCon=1)

#Đặt độ phân giải cho Cammera.
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
width = int(cap.get(3))
height = int(cap.get(4))

#Khởi tạo biến đảo ngược Camera.
Flip_CAM = False

# Trạng thái ban đầu của các nút bấm và đèn LED
Switch_state = np.array(
    [[False, False], [False, False], [False, False], [False, False], [False, False], [False, False]], dtype=bool)
LED_State = np.array([False, False, False, False, False, False], dtype=bool)

#Vẽ kích thước nút nhấn với kích thước 100x100
def draw_button(frame, x1, y1, x2, y2, text, status):
    if status == False:
        state = ": OFF"
    else:
        state = ": ON"
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
    if status == False:
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), -1)  # Màu đỏ khi OFF
    else:
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), -1)  # Màu xanh khi ON
    cv2.putText(frame, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)


def tracking(Hand_tracking, x1, y1, x2, y2, switch_state, led_state_index):
    x, y = Hand_tracking[8][1], Hand_tracking[8][2]

    # Cập nhật trạng thái chuyển mạch
    switch_state[0] = switch_state[1]

    # Kiểm tra nếu ngón tay trỏ nằm trong vùng hình chữ nhật
    if x1 <= x <= x2 and y1 <= y <= y2:
        switch_state[1] = True
    else:
        switch_state[1] = False

    # Nếu ngón tay trỏ vừa thoát khỏi vùng hình chữ nhật, đảo trạng thái LED
    if switch_state[0] == True and switch_state[1] == False:
        time.sleep(0.02)  # Thêm độ trễ ngắn để tránh việc nhấn nhanh nhiều lần
        LED_State[led_state_index] = not LED_State[led_state_index]
        if LED_State[led_state_index] == True:
            ser.write(f"{led_state_index+1}B".encode())
        else:
            ser.write(f"{led_state_index+1}T".encode())
while True:
    ret, frame = cap.read()

    # Nếu nhấn f hoặc F thì đảo ngược Camera.
    if cv2.waitKey(1) == ord("f") or cv2.waitKey(1) == ord("F"):
        Flip_CAM = not Flip_CAM
    if Flip_CAM == True:
        frame = cv2.flip(frame, 1)
    else:
        pass

    #Nhận diện bàn tay.
    frame = detector.findHands(frame)
    lmlist = detector.findPosition(frame, draw=False)

    #Chọn tọa độ căn lề và khoảng cách của các phím.
    start_x = (width // 6 - 100) // 2
    range_button = start_x * 2
    start_y = 25
    # Vẽ nút LED1 đến LED6
    for i in range(0, 6):
        draw_button(frame, start_x, start_y, start_x + 100, start_y + 100, f"LED{i + 1}", status=LED_State[i])

        # Nếu có bàn tay trong khung hình, kiểm tra việc nhấn nút
        if lmlist:
            tracking(lmlist, start_x, start_y, start_x + 100, start_y + 100, Switch_state[i], i)

        # Tính toán vị trí nút tiếp theo
        start_x += (100 + range_button)

    # Hiển thị khung hình
    cv2.imshow("Cua so", frame)

    # Thoát chương trình khi nhấn phím 's'
    if cv2.waitKey(1) == ord("s"):
        break


cap.release()
cv2.destroyAllWindows()
