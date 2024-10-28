import tkinter as tk
from tkinter import simpledialog, messagebox, ttk
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # Import thêm để vẽ 3D
from sympy import symbols, pi

# Khởi tạo cửa sổ chính
root = tk.Tk()
root.title("Ứng dụng vẽ hình và tính chu vi, diện tích")
root.geometry("500x400")
root.configure(bg="lightcyan")

# Khởi tạo Frame
main_frame = ttk.Frame(root, padding=10)
main_frame.pack(fill=tk.BOTH, expand=True)

# Khung để hiển thị kết quả
result_frame = ttk.Frame(root, padding=10)
result_label = tk.Label(result_frame, text="", font=("Arial", 12), bg="lightyellow", relief="solid", wraplength=400)
result_label.pack(pady=10, padx=10)
result_frame.pack_forget()  # Ẩn khung kết quả ban đầu


# Hàm hiển thị kết quả tính toán
def show_result(text):
    result_label.config(text=text)
    result_frame.pack(side=tk.BOTTOM, fill=tk.X)


# Hàm để thoát ứng dụng
def exit_app():
    root.quit()


# Hàm để quay lại menu chính
def back_to_main_menu():
    clear_window()
    tk.Label(main_frame, text="Chọn loại hình:", font=("Arial", 14)).pack(pady=20)
    ttk.Button(main_frame, text="2D", command=show_2d_menu).pack(pady=10)
    ttk.Button(main_frame, text="3D", command=show_3d_menu).pack(pady=10)
    ttk.Button(main_frame, text="Thoát", command=exit_app).pack(pady=20)


# Hàm xóa các thành phần cũ
def clear_window():
    for widget in main_frame.winfo_children():
        widget.pack_forget()
    result_frame.pack_forget()


# Menu cho hình 2D
def show_2d_menu():
    clear_window()
    tk.Label(main_frame, text="Chọn hình 2D", font=("Arial", 14)).pack()
    ttk.Button(main_frame, text="Hình tròn", command=draw_circle).pack(pady=5)
    ttk.Button(main_frame, text="Chữ nhật", command=draw_rectangle).pack(pady=5)
    ttk.Button(main_frame, text="Tam giác", command=draw_triangle).pack(pady=5)
    ttk.Button(main_frame, text="Hình bình hành", command=draw_parallelogram).pack(pady=5)
    ttk.Button(main_frame, text="Quay lại", command=back_to_main_menu).pack(pady=20)


# Menu cho hình 3D
def show_3d_menu():
    clear_window()
    tk.Label(main_frame, text="Chọn hình 3D", font=("Arial", 14)).pack()
    ttk.Button(main_frame, text="Hình cầu", command=draw_sphere).pack(pady=5)
    ttk.Button(main_frame, text="Hình trụ", command=draw_cylinder).pack(pady=5)
    ttk.Button(main_frame, text="Hình nón", command=draw_cone).pack(pady=5)
    ttk.Button(main_frame, text="Lăng trụ lục giác", command=draw_hexagonal_prism).pack(pady=5)
    ttk.Button(main_frame, text="Quay lại", command=back_to_main_menu).pack(pady=20)


# Hàm vẽ và tính chu vi, diện tích hình tròn
def draw_circle():
    r = simpledialog.askfloat("Nhập bán kính", "Bán kính của hình tròn:")
    if r and r > 0:
        chu_vi = 2 * np.pi * r
        dien_tich = np.pi * r ** 2
        show_result(f"Chu vi: {chu_vi:.2f}\nDiện tích: {dien_tich:.2f}")

        fig, ax = plt.subplots()
        circle = plt.Circle((0, 0), r, fill=False, edgecolor="blue", linewidth=2)
        ax.add_artist(circle)
        ax.set_xlim(-r - 1, r + 1)
        ax.set_ylim(-r - 1, r + 1)
        ax.set_aspect("equal", "box")
        plt.title("Hình tròn")
        plt.grid(True)
        plt.show()


# Hàm vẽ và tính chu vi, diện tích hình chữ nhật
def draw_rectangle():
    width = simpledialog.askfloat("Nhập chiều rộng", "Chiều rộng của hình chữ nhật:")
    height = simpledialog.askfloat("Nhập chiều dài", "Chiều dài của hình chữ nhật:")
    if width > 0 and height > 0:
        chu_vi = 2 * (width + height)
        dien_tich = width * height
        show_result(f"Chu vi: {chu_vi:.2f}\nDiện tích: {dien_tich:.2f}")

        fig, ax = plt.subplots()
        rectangle = plt.Rectangle((0, 0), width, height, fill=False, edgecolor="green", linewidth=2)
        ax.add_artist(rectangle)
        ax.set_xlim(-1, width + 1)
        ax.set_ylim(-1, height + 1)
        ax.set_aspect("equal", "box")
        plt.title("Hình chữ nhật")
        plt.grid(True)
        plt.show()


# Hàm vẽ và tính chu vi, diện tích hình tam giác
def draw_triangle():
    base = simpledialog.askfloat("Nhập cạnh đáy", "Cạnh đáy của tam giác:")
    height = simpledialog.askfloat("Nhập chiều cao", "Chiều cao của tam giác:")
    if base > 0 and height > 0:
        dien_tich = 0.5 * base * height
        chu_vi = 3 * base  # Giả sử tam giác đều
        show_result(f"Chu vi (giả sử tam giác đều): {chu_vi:.2f}\nDiện tích: {dien_tich:.2f}")

        fig, ax = plt.subplots()
        triangle = plt.Polygon([[0, 0], [base, 0], [base / 2, height]], fill=False, edgecolor="purple")
        ax.add_artist(triangle)
        ax.set_xlim(-1, base + 1)
        ax.set_ylim(-1, height + 1)
        ax.set_aspect("equal", "box")
        plt.title("Hình tam giác")
        plt.grid(True)
        plt.show()


# Hàm vẽ và tính diện tích, thể tích hình cầu
def draw_sphere():
    r = simpledialog.askfloat("Nhập bán kính", "Bán kính của hình cầu:")
    if r and r > 0:
        dien_tich = 4 * np.pi * r ** 2
        the_tich = (4 / 3) * np.pi * r ** 3
        show_result(f"Diện tích bề mặt: {dien_tich:.2f}\nThể tích: {the_tich:.2f}")

        fig = plt.figure()
        ax = fig.add_subplot(111, projection="3d")
        u = np.linspace(0, 2 * np.pi, 100)
        v = np.linspace(0, np.pi, 100)
        x = r * np.outer(np.cos(u), np.sin(v))
        y = r * np.outer(np.sin(u), np.sin(v))
        z = r * np.outer(np.ones(np.size(u)), np.cos(v))

        ax.plot_surface(x, y, z, color="cyan")
        ax.set_title("Hình cầu")
        plt.show()


# Hàm vẽ và tính diện tích, thể tích hình trụ
def draw_cylinder():
    r = simpledialog.askfloat("Nhập bán kính", "Bán kính của hình trụ:")
    h = simpledialog.askfloat("Nhập chiều cao", "Chiều cao của hình trụ:")
    if r > 0 and h > 0:
        dien_tich = 2 * np.pi * r * h + 2 * np.pi * r ** 2
        the_tich = np.pi * r ** 2 * h
        show_result(f"Diện tích bề mặt: {dien_tich:.2f}\nThể tích: {the_tich:.2f}")

        fig = plt.figure()
        ax = fig.add_subplot(111, projection="3d")
        z = np.linspace(0, h, 100)
        theta = np.linspace(0, 2 * np.pi, 100)
        theta, z = np.meshgrid(theta, z)
        x = r * np.cos(theta)
        y = r * np.sin(theta)

        ax.plot_surface(x, y, z, color="orange")
        ax.set_title("Hình trụ")
        plt.show()


# Hàm vẽ lăng trụ lục giác
def draw_hexagonal_prism():
    r = simpledialog.askfloat("Nhập bán kính", "Bán kính của lục lăng:")
    h = simpledialog.askfloat("Nhập chiều cao", "Chiều cao của lăng trụ:")
    if r > 0 and h > 0:
        dien_tich_day = (3 * np.sqrt(3) / 2) * r ** 2
        dien_tich_toan_phan = 2 * dien_tich_day + 6 * r * h
        the_tich = dien_tich_day * h
        show_result(f"Diện tích toàn phần: {dien_tich_toan_phan:.2f}\nThể tích: {the_tich:.2f}")
        # Vẽ 3D bỏ qua để không quá dài


# Chạy ứng dụng
back_to_main_menu()
root.mainloop()
