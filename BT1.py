import tkinter as tk
from tkinter import messagebox
import sympy as sp
import matplotlib.pyplot as plt
import numpy as np


# Hàm tạo giao diện cho hình tròn
def giao_dien_hinh_tron():
  def tinh_toan_hinh_tron():
    try:
      r = float(entry_r.get())
      if r <= 0:
        raise ValueError
      dien_tich = sp.pi * r ** 2
      chu_vi = 2 * sp.pi * r
      messagebox.showinfo("Kết quả", f"Diện tích: {dien_tich:.2f}\nChu vi: {chu_vi:.2f}")
      # Vẽ hình tròn
      theta = np.linspace(0, 2 * np.pi, 100)
      x = r * np.cos(theta)
      y = r * np.sin(theta)
      plt.plot(x, y)
      plt.gca().set_aspect('equal', adjustable='box')
      plt.title(f'Hình tròn bán kính r={r}')
      plt.grid(True)
      plt.show()
    except ValueError:
      messagebox.showerror("Lỗi", "Vui lòng nhập giá trị bán kính hợp lệ.")

  clear_main_window()

  label_r = tk.Label(root, text="Bán kính (r):")
  label_r.pack(pady=10)
  entry_r = tk.Entry(root)
  entry_r.pack(pady=5)
  button_tinh = tk.Button(root, text="Tính toán", command=tinh_toan_hinh_tron)
  button_tinh.pack(pady=10)
  button_thoat = tk.Button(root, text="Thoát", command=main_menu)
  button_thoat.pack(pady=5)


# Hàm tạo giao diện cho hình chữ nhật
def giao_dien_hinh_chu_nhat():
  def tinh_toan_hinh_chu_nhat():
    try:
      dai = float(entry_dai.get())
      rong = float(entry_rong.get())
      if dai <= 0 or rong <= 0:
        raise ValueError
      dien_tich = dai * rong
      chu_vi = 2 * (dai + rong)
      messagebox.showinfo("Kết quả", f"Diện tích: {dien_tich:.2f}\nChu vi: {chu_vi:.2f}")
    except ValueError:
      messagebox.showerror("Lỗi", "Vui lòng nhập chiều dài và chiều rộng hợp lệ.")

  clear_main_window()

  label_dai = tk.Label(root, text="Chiều dài:")
  label_dai.pack(pady=10)
  entry_dai = tk.Entry(root)
  entry_dai.pack(pady=5)
  label_rong = tk.Label(root, text="Chiều rộng:")
  label_rong.pack(pady=10)
  entry_rong = tk.Entry(root)
  entry_rong.pack(pady=5)
  button_tinh = tk.Button(root, text="Tính toán", command=tinh_toan_hinh_chu_nhat)
  button_tinh.pack(pady=10)
  button_thoat = tk.Button(root, text="Thoát", command=main_menu)
  button_thoat.pack(pady=5)


# Hàm tạo giao diện cho tam giác
def giao_dien_hinh_tam_giac():
  def tinh_toan_hinh_tam_giac():
    try:
      a = float(entry_a.get())
      b = float(entry_b.get())
      c = float(entry_c.get())
      if a <= 0 or b <= 0 or c <= 0 or a + b <= c or a + c <= b or b + c <= a:
        raise ValueError
      chu_vi = a + b + c
      p = chu_vi / 2
      dien_tich = sp.sqrt(p * (p - a) * (p - b) * (p - c))
      messagebox.showinfo("Kết quả", f"Diện tích: {dien_tich:.2f}\nChu vi: {chu_vi:.2f}")
    except ValueError:
      messagebox.showerror("Lỗi", "Vui lòng nhập độ dài 3 cạnh hợp lệ.")

  clear_main_window()

  label_a = tk.Label(root, text="Cạnh a:")
  label_a.pack(pady=10)
  entry_a = tk.Entry(root)
  entry_a.pack(pady=5)
  label_b = tk.Label(root, text="Cạnh b:")
  label_b.pack(pady=10)
  entry_b = tk.Entry(root)
  entry_b.pack(pady=5)
  label_c = tk.Label(root, text="Cạnh c:")
  label_c.pack(pady=10)
  entry_c = tk.Entry(root)
  entry_c.pack(pady=5)
  button_tinh = tk.Button(root, text="Tính toán", command=tinh_toan_hinh_tam_giac)
  button_tinh.pack(pady=10)
  button_thoat = tk.Button(root, text="Thoát", command=main_menu)
  button_thoat.pack(pady=5)


# Hàm xóa giao diện hiện tại
def clear_main_window():
  for widget in root.winfo_children():
    widget.pack_forget()


# Giao diện chính của ứng dụng
def main_menu():
  clear_main_window()

  label_main = tk.Label(root, text="Chọn hình cần tính toán", font=("Helvetica", 16))
  label_main.pack(pady=20)

  button_hinh_tron = tk.Button(root, text="Hình tròn", width=20, command=giao_dien_hinh_tron)
  button_hinh_tron.pack(pady=10)

  button_hinh_chu_nhat = tk.Button(root, text="Hình chữ nhật", width=20, command=giao_dien_hinh_chu_nhat)
  button_hinh_chu_nhat.pack(pady=10)

  button_hinh_tam_giac = tk.Button(root, text="Hình tam giác", width=20, command=giao_dien_hinh_tam_giac)
  button_hinh_tam_giac.pack(pady=10)


# Khởi tạo giao diện Tkinter
root = tk.Tk()
root.title("Ứng dụng hình học")
root.geometry("400x400")
root.configure(bg="lightblue")  # Màu nền chính cho cửa sổ

# Giao diện chính
main_menu()

# Bắt đầu vòng lặp ứng dụng
root.mainloop()
