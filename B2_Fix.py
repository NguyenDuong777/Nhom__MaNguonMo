import numpy as np
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog


def get_matrix_from_input(input_str):
  try:
    matrix = np.array([[int(num) for num in row.split()] for row in input_str.strip().split('\n')])
    return matrix
  except ValueError:
    messagebox.showerror("Error", "Dữ liệu nhập không hợp lệ!")
    return None


def matrix_addition():
  A = get_matrix_from_input(entry_matrix_A.get("1.0", tk.END))
  B = get_matrix_from_input(entry_matrix_B.get("1.0", tk.END))
  if A is not None and B is not None:
    if A.shape != B.shape:
      messagebox.showerror("Error", "Kích thước không tương thích để cộng ma trận!")
      return None

    result = A + B
    display_result(result)


def matrix_subtraction():
  A = get_matrix_from_input(entry_matrix_A.get("1.0", tk.END))
  B = get_matrix_from_input(entry_matrix_B.get("1.0", tk.END))
  if A is not None and B is not None:
    if A.shape != B.shape:
      messagebox.showerror("Error", "Kích thước không tương thích để trừ ma trận!")
      return None

    result = A - B
    display_result(result)


def matrix_division():
  A = get_matrix_from_input(entry_matrix_A.get("1.0", tk.END))
  B = get_matrix_from_input(entry_matrix_B.get("1.0", tk.END))
  if A is not None and B is not None:
    if B.shape[0] != B.shape[1]:
      messagebox.showerror("Error", "Ma trận B không phải là ma trận vuông nên không thể tính nghịch đảo!")
      return None

    try:
      B_inv = np.linalg.inv(B)
      result = np.dot(A, B_inv)
      display_result(result)
    except np.linalg.LinAlgError:
      messagebox.showerror("Error", "Ma trận B không khả nghịch!")
      return None

# Thêm vào các hàm cho giao diện mới
def matrix_inverse():
    A = get_matrix_from_input(entry_matrix_A.get("1.0", tk.END))
    if A is not None:
        if A.shape[0] != A.shape[1]:
            messagebox.showerror("Error", "Ma trận không phải là ma trận vuông, không thể tính nghịch đảo!")
            return None

        try:
            A_inv = np.linalg.inv(A)
            display_result(A_inv)
        except np.linalg.LinAlgError:
            messagebox.showerror("Error", "Ma trận không khả nghịch!")
            return None

def matrix_rank():
    A = get_matrix_from_input(entry_matrix_A.get("1.0", tk.END))
    if A is not None:
        rank = np.linalg.matrix_rank(A)
        messagebox.showinfo("Hạng của ma trận", f"Hạng của ma trận A là: {rank}")

def solve_linear_system():
    A = get_matrix_from_input(entry_matrix_A.get("1.0", tk.END))
    if A is not None:
        # Hiển thị hộp thoại để nhập vector b
        input_b = simpledialog.askstring("Nhập vector b", "Nhập vector b (các giá trị cách nhau bởi dấu cách):")
        try:
            b = np.array([float(num) for num in input_b.split()])

            if A.shape[0] != len(b):
                messagebox.showerror("Error", "Số hàng của ma trận A phải bằng số phần tử của vector b!")
                return None

            x = np.linalg.solve(A, b)
            result_str = " ".join(map(str, x))
            messagebox.showinfo("Giải hệ phương trình", f"Giá trị của x là: {result_str}")
        except ValueError:
            messagebox.showerror("Error", "Dữ liệu nhập không hợp lệ!")
        except np.linalg.LinAlgError:
            messagebox.showerror("Error", "Ma trận không thể giải được!")

def matrix_multiplication():
  A = get_matrix_from_input(entry_matrix_A.get("1.0", tk.END))
  B = get_matrix_from_input(entry_matrix_B.get("1.0", tk.END))
  if A is not None and B is not None:
    if A.shape[1] != B.shape[0]:
      messagebox.showerror("Error", "Kích thước không tương thích để nhân ma trận!")
      return None

    result = np.dot(A, B)
    display_result(result)


def display_result(result):
  result_str = "\n".join(["\t".join(map(str, row)) for row in result])
  entry_result.config(state=tk.NORMAL)
  entry_result.delete("1.0", tk.END)
  entry_result.insert(tk.END, result_str)
  entry_result.config(state=tk.DISABLED)

# Hàm mở giao diện khác (sửa lại để thêm các chức năng mới)
def open_new_interface():
    new_window = tk.Toplevel(win)
    new_window.title("Giao diện ma trận nâng cao")
    new_window.geometry("400x300")
    new_window.configure(bg="lightblue")

    label = tk.Label(new_window, text="Chọn phép tính cho ma trận A", bg="lightblue")
    label.pack(pady=10)

    btn_inverse = tk.Button(new_window, text="Tính nghịch đảo", command=matrix_inverse)
    btn_inverse.pack(pady=5)

    btn_rank = tk.Button(new_window, text="Tìm hạng của ma trận", command=matrix_rank)
    btn_rank.pack(pady=5)

    btn_solve = tk.Button(new_window, text="Giải hệ phương trình", command=solve_linear_system)
    btn_solve.pack(pady=5)

    btn_close = tk.Button(new_window, text="Đóng", command=new_window.destroy)
    btn_close.pack(pady=10)

# Hàm để xóa dữ liệu
def clear_matrices():
  entry_matrix_A.delete("1.0", tk.END)
  entry_matrix_B.delete("1.0", tk.END)
  entry_result.config(state=tk.NORMAL)
  entry_result.delete("1.0", tk.END)
  entry_result.config(state=tk.DISABLED)

# Tạo giao diện
win = tk.Tk()
win.title("Tính toán ma trận")
win.configure(bg="lightcyan")

# Ma trận A
label_matrix_A = tk.Label(win, text="Ma trận A:", bg="lightgray")
label_matrix_A.grid(row=0, column=0, padx=10, pady=10)

entry_matrix_A = tk.Text(win, height=5, width=20)
entry_matrix_A.grid(row=1, column=0, padx=10, pady=10)

# Ma trận B
label_matrix_B = tk.Label(win, text="Ma trận B:", bg="lightgray")
label_matrix_B.grid(row=0, column=1, padx=10, pady=10)

entry_matrix_B = tk.Text(win, height=5, width=20)
entry_matrix_B.grid(row=1, column=1, padx=10, pady=10)

# Nút tính toán
btn_add = tk.Button(win, text="Cộng", command=matrix_addition)
btn_add.grid(row=2, column=0, pady=10)

btn_subtract = tk.Button(win, text="Trừ", command=matrix_subtraction)
btn_subtract.grid(row=2, column=1, pady=10)

btn_multiply = tk.Button(win, text="Nhân", command=matrix_multiplication)
btn_multiply.grid(row=3, column=0, pady=10)

btn_divide = tk.Button(win, text="Chia", command=matrix_division)
btn_divide.grid(row=3, column=1, pady=10)

# Kết quả
label_result = tk.Label(win, text="Kết quả:", bg="lightgray")
label_result.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

entry_result = tk.Text(win, height=5, width=40, state=tk.DISABLED)
entry_result.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

# Nút xóa dữ liệu
btn_clear = tk.Button(win, text="Xóa dữ liệu", command=clear_matrices)
btn_clear.grid(row=6, column=0, columnspan=2, pady=10)

# Nút mở giao diện mới
btn_open_interface = tk.Button(win, text="Mở giao diện mới", command=open_new_interface)
btn_open_interface.grid(row=7, column=0, columnspan=2, pady=10)

win.mainloop()
