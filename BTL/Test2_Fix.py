import tkinter as tk
import speech_recognition as sr
import threading
import serial
import re  # Thêm thư viện re để xử lý chuỗi

# Kết nối với STM32 qua COM port
ser = serial.Serial("COM4", 115200, 8, "N", 1)

# Tạo cửa sổ giao diện tkinter
root = tk.Tk()
root.title("Điều khiển LED bằng Giọng nói")
root.geometry("400x300")

# Label hiển thị giọng nói nhận được
label = tk.Label(root, text="Chưa nhận giọng nói", font=("Arial", 16), width=40, height=10)
label.pack()


# Hàm nhận diện giọng nói và điều khiển LED
def recognize_and_control_led():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    while True:
        with mic as source:
            recognizer.adjust_for_ambient_noise(source)
            print("Đang lắng nghe...")
            audio = recognizer.listen(source)

        try:
            # Nhận diện giọng nói
            command = recognizer.recognize_google(audio, language="vi-VN").lower()
            print(f"Nhận diện: {command}")
            label.config(text=f"Nhận diện: {command}")

            # Xử lý lệnh "bật đèn số ..." và "tắt đèn số ..."
            if "bật đèn số" in command:
                numbers = re.findall(r'\d+', command)  # Tìm tất cả các số trong chuỗi
                for num in numbers:
                    if 1 <= int(num) <= 6:
                        ser.write(f"{num}B".encode())  # Bật LED tương ứng

            elif "tắt đèn số" in command:
                numbers = re.findall(r'\d+', command)  # Tìm tất cả các số trong chuỗi
                for num in numbers:
                    if 1 <= int(num) <= 6:
                        ser.write(f"{num}T".encode())  # Tắt LED tương ứng

            elif "bật đèn" in command:
                for i in range(1, 7):
                    ser.write(f"{i}B".encode())  # Bật tất cả LED

            elif "tắt đèn" in command:
                for i in range(1, 7):
                    ser.write(f"{i}T".encode())  # Tắt tất cả LED

        except sr.UnknownValueError:
            print("Không thể nhận diện giọng nói")
            label.config(text="Không thể nhận diện giọng nói")
        except sr.RequestError:
            print("Lỗi kết nối với Google Speech API")
            label.config(text="Lỗi kết nối với Google Speech API")


# Tạo một thread riêng để chạy nhận diện giọng nói mà không làm gián đoạn giao diện tkinter
voice_thread = threading.Thread(target=recognize_and_control_led)
voice_thread.daemon = True  # Cho phép đóng thread khi đóng chương trình
voice_thread.start()

# Chạy giao diện tkinter
root.mainloop()
