import tkinter as tk
from tkinter import ttk, messagebox
import serial
import serial.tools.list_ports
import subprocess

def get_available_com_ports():
    ports = serial.tools.list_ports.comports()
    return [port.device for port in ports]
# Lấy danh sách cổng COM khả dụng
available_ports = get_available_com_ports()
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

    # Truyền thông tin và chạy file TEST2.py
    subprocess.Popen(["python", "Project1.py", com_port, resolution])
    root.destroy()

# Tạo giao diện
root = tk.Tk()
root.title("Cấu hình khởi động")
root.geometry("400x300")
root.config(bg="#f4f4f9")  # Màu nền sáng

# Chọn cổng COM
tk.Label(root, text="Chọn cổng COM:", font=("Arial", 12), bg="#f4f4f9").pack(pady=5)
# com_combobox = ttk.Combobox(root, values=["COM1", "COM2", "COM3", "COM4"], state="readonly", font=("Arial", 12))
com_combobox = ttk.Combobox(
    root,
    values=available_ports,
    state="readonly",
    font=("Arial", 12)
)
com_combobox.pack(pady=5, padx=20, fill="x")

# Chọn độ phân giải
tk.Label(root, text="Chọn độ phân giải:", font=("Arial", 12), bg="#f4f4f9").pack(pady=5)
res_combobox = ttk.Combobox(root, values=["480", "720"], state="readonly", font=("Arial", 12))
res_combobox.pack(pady=5, padx=20, fill="x")

# Nút bắt đầu
start_button = tk.Button(root, text="Bắt đầu", command=start_program, font=("Arial", 12), bg="#4CAF50", fg="white", relief="flat", padx=20, pady=10)
start_button.pack(pady=20)

root.mainloop()
