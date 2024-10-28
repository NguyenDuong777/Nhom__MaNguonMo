import tkinter as tk
from tkinter import messagebox
import sympy as sp
import matplotlib.pyplot as plt
import numpy as np


# Hàm tính toán diện tích và chu vi hình tròn
def tinh_toan_hinh_tron(r):
    dien_tich = sp.pi * r ** 2
    chu_vi = 2 * sp.pi * r
    return dien_tich, chu_vi


# Hàm tính toán diện tích và chu vi hình chữ nhật
def tinh_toan_hinh_chu_nhat(dai, rong):
    dien_tich = dai * rong
    chu_vi = 2 * (dai + rong)
    return dien_tich, chu_vi


# Hàm tính toán diện tích và chu vi tam giác
def tinh_toan_hinh_tam_giac(a, b, c):
    chu_vi = a + b + c
    p = chu_vi / 2
    dien_tich = sp.sqrt(p * (p - a) * (p - b) * (p - c))
    return dien_tich, chu_vi


# Hàm tạo giao diện cho hình tròn
def giao_dien_hinh_tron():
    clear_main_window()

    frame_circle = tk.Frame(root, bg="lightblue")
    frame_circle.pack(pady=20)

    label_r = tk.Label(frame_circle, text="Bán kính (r):", bg="lightblue")
    label_r.grid(row=0, column=0, padx=5, pady=5)
    entry_r = tk.Entry(frame_circle)
    entry_r.grid(row=0, column=1, padx=5, pady=5)

    def tinh_toan():
        try:
            r = float(entry_r.get())
            if r <= 0:
                raise ValueError("Bán kính phải là số dương")
            dien_tich, chu_vi = tinh_toan_hinh_tron(r)
            messagebox.showinfo("Kết quả", f"Diện tích: {dien_tich:.2f}\nChu vi: {chu_vi:.2f}")
            
            # Vẽ hình tròn
            theta = np.linspace(0, 2 * np.pi, 100)
            x = r * np.cos(theta)
            y = r * np.sin(theta)
            plt.figure()
            plt.plot(x, y)
            plt.gca().set_aspect('equal', adjustable='box')
            plt.title(f'Hình tròn bán kính r={r}')
            plt.grid(True)
            plt.show()
        except ValueError:
            messagebox.showerror("Lỗi", "Vui lòng nhập giá trị bán kính hợp lệ.")

    button_tinh = tk.Button(frame_circle, text="Tính toán", command=tinh_toan)
    button_tinh.grid(row=1, column=0, columnspan=2, pady=10)
    button_thoat = tk.Button(frame_circle, text="Thoát", command=main_menu)
    button_thoat.grid(row=2, column=0, columnspan=2, pady=5)


# Hàm tạo giao diện cho hình chữ nhật
def giao_dien_hinh_chu_nhat():
    clear_main_window()

    frame_rectangle = tk.Frame(root, bg="lightblue")
    frame_rectangle.pack(pady=20)

    label_dai = tk.Label(frame_rectangle, text="Chiều dài:", bg="lightblue")
    label_dai.grid(row=0, column=0, padx=5, pady=5)
    entry_dai = tk.Entry(frame_rectangle)
    entry_dai.grid(row=0, column=1, padx=5, pady=5)

    label_rong = tk.Label(frame_rectangle, text="Chiều rộng:", bg="lightblue")
    label_rong.grid(row=1, column=0, padx=5, pady=5)
    entry_rong = tk.Entry(frame_rectangle)
    entry_rong.grid(row=1, column=1, padx=5, pady=5)

    def tinh_toan():
        try:
            dai = float(entry_dai.get())
            rong = float(entry_rong.get())
            if dai <= 0 or rong <= 0:
                raise ValueError("Chiều dài và chiều rộng phải là số dương")
            dien_tich, chu_vi = tinh_toan_hinh_chu_nhat(dai, rong)
            messagebox.showinfo("Kết quả", f"Diện tích: {dien_tich:.2f}\nChu vi: {chu_vi:.2f}")
        except ValueError:
            messagebox.showerror("Lỗi", "Vui lòng nhập chiều dài và chiều rộng hợp lệ.")

    button_tinh = tk.Button(frame_rectangle, text="Tính toán", command=tinh_toan)
    button_tinh.grid(row=2, column=0, columnspan=2, pady=10)
    button_thoat = tk.Button(frame_rectangle, text="Thoát", command=main_menu)
    button_thoat.grid(row=3, column=0, columnspan=2, pady=5)


# Hàm tạo giao diện cho tam giác
def giao_dien_hinh_tam_giac():
    clear_main_window()

    frame_triangle = tk.Frame(root, bg="lightblue")
    frame_triangle.pack(pady=20)

    label_a = tk.Label(frame_triangle, text="Cạnh a:", bg="lightblue")
    label_a.grid(row=0, column=0, padx=5, pady=5)
    entry_a = tk.Entry(frame_triangle)
    entry_a.grid(row=0, column=1, padx=5, pady=5)

    label_b = tk.Label(frame_triangle, text="Cạnh b:", bg="lightblue")
    label_b.grid(row=1, column=0, padx=5, pady=5)
    entry_b = tk.Entry(frame_triangle)
    entry_b.grid(row=1, column=1, padx=5, pady=5)

    label_c = tk.Label(frame_triangle, text="Cạnh c:", bg="lightblue")
    label_c.grid(row=2, column=0, padx=5, pady=5)
    entry_c = tk.Entry(frame_triangle)
    entry_c.grid(row=2, column=1, padx=5, pady=5)

    def tinh_toan():
        try:
            a = float(entry_a.get())
            b = float(entry_b.get())
            c = float(entry_c.get())
            if a <= 0 or b <= 0 or c <= 0 or a + b <= c or a + c <= b or b + c <= a:
                raise ValueError("Ba cạnh không tạo thành một tam giác")
            dien_tich, chu_vi = tinh_toan_hinh_tam_giac(a, b, c)
            messagebox.showinfo("Kết quả", f"Diện tích: {dien_tich:.2f}\nChu vi: {chu_vi:.2f}")
        except ValueError:
            messagebox.showerror("Lỗi", "Vui lòng nhập độ dài 3 cạnh hợp lệ.")

    button_tinh = tk.Button(frame_triangle, text="Tính toán", command=tinh_toan)
    button_tinh.grid(row=3, column=0, columnspan=2, pady=10)
    button_thoat = tk.Button(frame_triangle, text="Thoát", command=main_menu)
    button_thoat.grid(row=4, column=0, columnspan=2, pady=5)


# Hàm xóa giao diện hiện tại
def clear_main_window():
    for widget in root.winfo_children():
        widget.pack_forget()


# Giao diện chính của ứng dụng
def main_menu():
    clear_main_window()

    frame_main = tk.Frame(root, bg="lightblue")
    frame_main.pack(pady=20)

    label_main = tk.Label(frame_main, text="Chọn hình cần tính toán", font=("Helvetica", 16), bg="lightblue")
    label_main.pack(pady=20)

    button_hinh_tron = tk.Button(frame_main, text="Hình tròn", width=20, command=giao_dien_hinh_tron)
    button_hinh_tron.pack(pady=10)

    button_hinh_chu_nhat = tk.Button(frame_main, text="Hình chữ nhật", width=20, command=giao_dien_hinh_chu_nhat)
    button_hinh_chu_nhat.pack(pady=10)

    button_hinh_tam_giac = tk.Button(frame_main, text="Hình tam giác", width=20, command=giao_dien_hinh_tam_giac)
    button_hinh_tam_giac.pack(pady=10)


# Khởi tạo giao diện Tkinter
root =
