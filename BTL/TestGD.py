import tkinter as tk
from tkinter import ttk, messagebox
import serial
import subprocess


# Hàm kiểm tra cổng COM
def check_com_port(port):
  try:
    ser = serial.Serial(port, 115200, timeout=1)
    ser.close()
    return True
  except serial.SerialException:
    return False


# Hàm bắt đầu chương trình
def start_program():
  com_port = com_combobox.get()
  resolution = res_combobox.get()

  if not com_port:
    messagebox.showerror("Lỗi", "Vui lòng chọn cổng COM")
    return
  if not check_com_port(com_port):
    messagebox.showerror("Lỗi", f"Không thể kết nối với {com_port}")
    return

  if not resolution:
    messagebox.showerror("Lỗi", "Vui lòng chọn độ phân giải")
    return

  # Truyền thông tin và chạy file TEST3.py
  subprocess.Popen(["python", "TEST2.py", com_port, resolution])
  root.destroy()


# Tạo giao diện
root = tk.Tk()
root.title("Cấu hình khởi động")
root.geometry("400x300")

# Chọn cổng COM
tk.Label(root, text="Chọn cổng COM:").pack(pady=5)
com_combobox = ttk.Combobox(root, values=["COM1", "COM2", "COM3", "COM4"], state="readonly")
com_combobox.pack(pady=5)

# Chọn độ phân giải
tk.Label(root, text="Chọn độ phân giải:").pack(pady=5)
res_combobox = ttk.Combobox(root, values=["480", "720"], state="readonly")
res_combobox.pack(pady=5)

# Nút bắt đầu
start_button = tk.Button(root, text="Bắt đầu", command=start_program)
start_button.pack(pady=20)

root.mainloop()
