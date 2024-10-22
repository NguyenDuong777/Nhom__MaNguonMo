import tkinter as tk
from tkinter import simpledialog, messagebox
import numpy as np
import matplotlib.pyplot as plt
from sympy import symbols, pi

# Khởi tạo cửa sổ chính
root = tk.Tk()
root.title("Ứng dụng vẽ hình và tính chu vi, diện tích")
root.geometry("400x300")
root.configure(bg="lightcyan")  # Màu nền chính cho cửa sổ

# Hàm để thoát ứng dụng
def exit_app():
  root.quit()


# Hàm để quay lại menu chính
def back_to_main_menu():
  clear_window()
  tk.Label(root, text="Chọn loại hình:").pack(pady=20)
  tk.Button(root, text="2D", command=show_2d_menu).pack(pady=10)
  tk.Button(root, text="3D", command=show_3d_menu).pack(pady=10)
  tk.Button(root, text="Thoát", command=exit_app).pack(pady=20)


# Hàm để hiển thị menu 2D
def show_2d_menu():
  clear_window()
  tk.Label(root, text="Chọn hình 2D").pack()

  tk.Button(root, text="Hình tròn", command=draw_circle).pack()
  tk.Button(root, text="Chữ nhật", command=draw_rectangle).pack()
  tk.Button(root, text="Tam giác", command=draw_triangle).pack()
  tk.Button(root, text="Hình bình hành", command=draw_parallelogram).pack()
  tk.Button(root, text="Thoát", command=back_to_main_menu).pack(pady=10)


# Hàm để hiển thị menu 3D
def show_3d_menu():
  clear_window()
  tk.Label(root, text="Chọn hình 3D").pack()

  tk.Button(root, text="Hình cầu", command=draw_sphere).pack()
  tk.Button(root, text="Hình trụ", command=draw_cylinder).pack()
  tk.Button(root, text="Hình nón", command=draw_cone).pack()
  # tk.Button(root, text="Lục lăng", command=draw_hexagon).pack()
  tk.Button(root, text="Lăng trụ lục giác", command=draw_hexagonal_prism).pack()

  tk.Button(root, text="Thoát", command=back_to_main_menu).pack(pady=10)


# Hàm để xóa các thành phần cũ
def clear_window():
  for widget in root.winfo_children():
    widget.pack_forget()


# Hàm vẽ hình tròn
def draw_circle():
  r = simpledialog.askfloat("Nhập bán kính", "Bán kính của hình tròn:")
  if r:
    chu_vi = 2 * np.pi * r
    dien_tich = np.pi * r ** 2

    messagebox.showinfo("Kết quả", f"Chu vi: {chu_vi:.2f}\nDiện tích: {dien_tich:.2f}")

    # Vẽ hình tròn
    fig, ax = plt.subplots()
    circle = plt.Circle((0, 0), r, fill=False)
    ax.add_artist(circle)
    ax.set_xlim(-r - 1, r + 1)
    ax.set_ylim(-r - 1, r + 1)
    ax.set_aspect('equal', 'box')
    plt.title("Hình tròn")
    plt.grid(True)
    plt.show()


# Hàm vẽ hình chữ nhật
def draw_rectangle():
  width = simpledialog.askfloat("Nhập chiều rộng", "Chiều rộng của hình chữ nhật:")
  height = simpledialog.askfloat("Nhập chiều dài", "Chiều dài của hình chữ nhật:")
  if width and height:
    chu_vi = 2 * (width + height)
    dien_tich = width * height

    messagebox.showinfo("Kết quả", f"Chu vi: {chu_vi:.2f}\nDiện tích: {dien_tich:.2f}")

    # Vẽ hình chữ nhật
    fig, ax = plt.subplots()
    rectangle = plt.Rectangle((0, 0), width, height, fill=False, edgecolor='blue', linewidth=2)
    ax.add_artist(rectangle)
    ax.set_xlim(-1, width + 1)
    ax.set_ylim(-1, height + 1)
    ax.set_aspect('equal', 'box')
    plt.title("Hình chữ nhật")
    plt.grid(True)
    plt.show()


# Hàm vẽ hình tam giác
def draw_triangle():
  base = simpledialog.askfloat("Nhập cạnh đáy", "Cạnh đáy của tam giác:")
  height = simpledialog.askfloat("Nhập chiều cao", "Chiều cao của tam giác:")
  if base and height:
    dien_tich = 0.5 * base * height
    chu_vi = 3 * base  # Giả sử tam giác đều để tính chu vi

    messagebox.showinfo("Kết quả", f"Chu vi (giả sử tam giác đều): {chu_vi:.2f}\nDiện tích: {dien_tich:.2f}")

    # Vẽ tam giác
    fig, ax = plt.subplots()
    triangle = plt.Polygon([[0, 0], [base, 0], [base / 2, height]], fill=False)
    ax.add_artist(triangle)
    ax.set_xlim(-1, base + 1)
    ax.set_ylim(-1, height + 1)
    ax.set_aspect('equal', 'box')
    plt.title("Hình tam giác")
    plt.grid(True)
    plt.show()


# Hàm vẽ hình bình hành
def draw_parallelogram():
  base = simpledialog.askfloat("Nhập cạnh đáy", "Cạnh đáy của hình bình hành:")
  height = simpledialog.askfloat("Nhập chiều cao", "Chiều cao của hình bình hành:")
  if base and height:
    dien_tich = base * height
    chu_vi = 2 * (base + height)  # Giả sử cạnh bên bằng chiều cao để tính chu vi

    messagebox.showinfo("Kết quả", f"Chu vi (giả sử cạnh bên bằng chiều cao): {chu_vi:.2f}\nDiện tích: {dien_tich:.2f}")

    # Vẽ hình bình hành
    fig, ax = plt.subplots()
    parallelogram = plt.Polygon([[0, 0], [base, 0], [base - height / 2, height], [-height / 2, height]], fill=False)
    ax.add_artist(parallelogram)
    ax.set_xlim(-1, base + 1)
    ax.set_ylim(-1, height + 1)
    ax.set_aspect('equal', 'box')
    plt.title("Hình bình hành")
    plt.grid(True)
    plt.show()


# Hàm vẽ hình cầu
def draw_sphere():
  r = simpledialog.askfloat("Nhập bán kính", "Bán kính của hình cầu:")
  if r:
    dien_tich = 4 * np.pi * r ** 2
    the_tich = (4 / 3) * np.pi * r ** 3

    messagebox.showinfo("Kết quả", f"Diện tích bề mặt: {dien_tich:.2f}\nThể tích: {the_tich:.2f}")

    # Vẽ hình cầu
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    x = r * np.outer(np.cos(u), np.sin(v))
    y = r * np.outer(np.sin(u), np.sin(v))
    z = r * np.outer(np.ones(np.size(u)), np.cos(v))

    ax.plot_surface(x, y, z, color='b')
    ax.set_title("Hình cầu")
    plt.show()


# Hàm vẽ hình trụ
def draw_cylinder():
  r = simpledialog.askfloat("Nhập bán kính", "Bán kính của hình trụ:")
  h = simpledialog.askfloat("Nhập chiều cao", "Chiều cao của hình trụ:")
  if r and h:
    dien_tich = 2 * np.pi * r * h + 2 * np.pi * r ** 2
    the_tich = np.pi * r ** 2 * h

    messagebox.showinfo("Kết quả", f"Diện tích bề mặt: {dien_tich:.2f}\nThể tích: {the_tich:.2f}")

    # Vẽ hình trụ
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    z = np.linspace(0, h, 100)
    theta = np.linspace(0, 2 * np.pi, 100)
    theta, z = np.meshgrid(theta, z)
    x = r * np.cos(theta)
    y = r * np.sin(theta)

    ax.plot_surface(x, y, z, color='r')
    ax.set_title("Hình trụ")
    plt.show()


# Hàm vẽ hình nón
def draw_cone():
  r = simpledialog.askfloat("Nhập bán kính", "Bán kính của hình nón:")
  h = simpledialog.askfloat("Nhập chiều cao", "Chiều cao của hình nón:")
  if r and h:
    dien_tich = np.pi * r * np.sqrt(r ** 2 + h ** 2) + np.pi * r ** 2
    the_tich = (1 / 3) * np.pi * r ** 2 * h

    messagebox.showinfo("Kết quả", f"Diện tích bề mặt: {dien_tich:.2f}\nThể tích: {the_tich:.2f}")

    # Vẽ hình nón
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    z = np.linspace(0, h, 100)
    theta = np.linspace(0, 2 * np.pi, 100)
    theta, z = np.meshgrid(theta, z)
    x = r * (1 - z / h) * np.cos(theta)
    y = r * (1 - z / h) * np.sin(theta)

    ax.plot_surface(x, y, z, color='g')
    ax.set_title("Hình nón")
    plt.show()


# Hàm vẽ hình lục lăng
# def draw_hexagon():
#   r = simpledialog.askfloat("Nhập bán kính", "Bán kính của lục lăng:")
#   if r:
#     chu_vi = 6 * r
#     dien_tich = (3 * np.sqrt(3) / 2) * r ** 2
#
#     messagebox.showinfo("Kết quả", f"Chu vi: {chu_vi:.2f}\nDiện tích: {dien_tich:.2f}")
#
#     # Vẽ hình lục lăng
#     fig, ax = plt.subplots()
#     angles = np.linspace(0, 2 * np.pi, 7)
#     x = r * np.cos(angles)
#     y = r * np.sin(angles)
#
#     ax.plot(x, y, 'b-')
#     ax.fill(x, y, 'b', alpha=0.1)
#     ax.set_aspect('equal', 'box')
#     plt.title("Lục lăng")
#     plt.grid(True)
#     plt.show()
# Hàm vẽ hình lăng trụ lục giác (hexagonal prism)
def draw_hexagonal_prism():
  r = simpledialog.askfloat("Nhập bán kính", "Bán kính của lục lăng:")
  h = simpledialog.askfloat("Nhập chiều cao", "Chiều cao của lục lăng:")
  if r and h:
    dien_tich_day = (3 * np.sqrt(3) / 2) * r ** 2
    chu_vi_day = 6 * r
    dien_tich_xung_quanh = 6 * r * h
    dien_tich_toan_phan = 2 * dien_tich_day + dien_tich_xung_quanh
    the_tich = dien_tich_day * h

    messagebox.showinfo("Kết quả", f"Chu vi đáy: {chu_vi_day:.2f}\nDiện tích xung quanh: {dien_tich_xung_quanh:.2f}\n"
                                   f"Diện tích toàn phần: {dien_tich_toan_phan:.2f}\nThể tích: {the_tich:.2f}")

    # Vẽ hình lăng trụ lục giác
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Tạo các điểm cho lục giác ở đáy và đỉnh
    angles = np.linspace(0, 2 * np.pi, 7)
    x_base = r * np.cos(angles)
    y_base = r * np.sin(angles)
    z_base = np.zeros(7)
    z_top = np.full(7, h)

    # Vẽ đáy và đỉnh
    ax.plot(x_base, y_base, z_base, 'b-')
    ax.plot(x_base, y_base, z_top, 'b-')

    # Vẽ các cạnh bên
    for i in range(6):
      ax.plot([x_base[i], x_base[i]], [y_base[i], y_base[i]], [z_base[i], z_top[i]], 'b-')

    ax.set_title("Lăng trụ lục giác")
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.show()

# Tạo giao diện chính với các nút 2D, 3D và thoát
tk.Label(root, text="Chọn loại hình:").pack(pady=20)
tk.Button(root, text="2D", command=show_2d_menu).pack(pady=10)
tk.Button(root, text="3D", command=show_3d_menu).pack(pady=10)
tk.Button(root, text="Thoát", command=exit_app).pack(pady=20)

# Chạy ứng dụng
root.mainloop()
