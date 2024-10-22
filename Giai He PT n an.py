import tkinter as tk
from tkinter import *
from tkinter import messagebox
import numpy as np


# Hàm để giải hệ phương trình
def solve_equations():
  try:
    n = int(entry_n.get())  # Lấy số n (số ẩn)
    matrix = []
    results = []

    # Lấy các hệ số ma trận từ các ô nhập liệu
    for i in range(n):
      row = []
      for j in range(n):
        entry_value = coefficient_entries[i][j].get()
        row.append(float(entry_value))
      matrix.append(row)

    # Lấy kết quả từ các ô nhập
    for i in range(n):
      results.append(float(result_entries[i].get()))

    # Giải hệ phương trình bằng numpy
    A = np.array(matrix)
    B = np.array(results)
    solutions = np.linalg.solve(A, B)

    # Hiển thị kết quả
    solution_str = "\n".join([f"x{i + 1} = {solutions[i]:.2f}" for i in range(n)])
    messagebox.showinfo("Kết quả", solution_str)

  except Exception as e:
    messagebox.showerror("Lỗi", str(e))


# Hàm để xóa các ô nhập liệu
# Hàm để xóa toàn bộ các ô nhập liệu và nhãn
def clear_entries():
  try:
    # Xóa tất cả các widget được tạo ở hàng 2 trở đi
    for widget in root.grid_slaves():
      if int(widget.grid_info()["row"]) >= 2:
        widget.grid_forget()

    # Đặt lại các danh sách hệ số và kết quả về rỗng
    global coefficient_entries, result_entries
    coefficient_entries = []
    result_entries = []

  except Exception as e:
    messagebox.showerror("Lỗi", "Không thể xóa dữ liệu.")



# Giao diện người dùng bằng Tkinter
root = tk.Tk()
root.title("Giải hệ n phương trình n ẩn")
root.configure(bg="lightblue")



# Nhập số n
label_n = tk.Label(root, text="Nhập số ẩn n:")
label_n.grid(row=0, column=0)
entry_n = tk.Entry(root)
entry_n.grid(row=0, column=1)


# Hàm để tạo các ô nhập hệ số và kết quả
def create_entries():
    global coefficient_entries, result_entries
    try:
        n = int(entry_n.get())
        if n <= 0:
            messagebox.showerror("Error", "Dữ liệu nhập không hợp lệ!")
            return

        coefficient_entries = []
        result_entries = []

        # Xóa tất cả các widget trước đó nếu có
        for widget in root.grid_slaves():
            if int(widget.grid_info()["row"]) >= 2:
                widget.grid_forget()

        # Tạo các ô nhập liệu và nhãn
        for i in range(n):
            row_entries = []

            for j in range(n):
                # Tạo ô nhập liệu cho hệ số
                entry = tk.Entry(root, width=5)
                entry.grid(row=i + 2, column=2 * j)  # Đặt ô nhập liệu cho hệ số
                row_entries.append(entry)

                # Tạo nhãn cho biến (x1, x2, y1, ...) ngay bên trong cùng ô với hệ số
                var_label = tk.Label(root, text=f"x{j + 1}")
                var_label.grid(row=i + 2, column=2 * j, sticky="e", padx=0)  # Nhãn sát bên cạnh ô dữ liệu

            coefficient_entries.append(row_entries)

            # Tạo nhãn cho dấu "="
            equal_label = tk.Label(root, text="=")
            equal_label.grid(row=i + 2, column=2 * n)

            # Tạo ô nhập cho kết quả
            entry = tk.Entry(root, width=5)
            entry.grid(row=i + 2, column=2 * n + 1)
            result_entries.append(entry)

    except Exception as e:
        messagebox.showerror("Lỗi", "Hãy nhập một số hợp lệ cho n.")



# Nút tạo các ô nhập
button_create_entries = tk.Button(root, text="Tạo các ô nhập", command=create_entries)
button_create_entries.grid(row=1, column=0, columnspan=2)

# Nút giải phương trình
button_solve = tk.Button(root, text="Giải phương trình", command=solve_equations)
button_solve.grid(row=1, column=2)

# Nút xóa dữ liệu
button_clear = tk.Button(root, text="Xóa dữ liệu", command=clear_entries)
button_clear.grid(row=1, column=3)

root.mainloop()
