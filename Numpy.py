import numpy as np
import tkinter as tk
from tkinter import messagebox

def get_matrix_from_input(input_str):
    try:
        matrix = np.array([[int(num) for num in row.split()] for row in input_str.strip().split('\n')])
        return matrix
    except ValueError:
        messagebox.showerror("Error", "Dữ liệu nhập không hợp lệ!")
        return None

def matrix_multiplication():
    A = get_matrix_from_input(entry_matrix_A.get("1.0", tk.END))
    B = get_matrix_from_input(entry_matrix_B.get("1.0", tk.END))
    if A is not None and B is not None:
        if A.shape[1] != B.shape[0]:
            messagebox.showerror("Error","Kích thước không tương thích để nhân ma trận!")
            return None

        result = np.dot(A, B)

        result_str = "\n".join(["\t".join(map(str, row)) for row in result])
        entry_result.config(state=tk.NORMAL)
        entry_result.delete("1.0", tk.END)
        entry_result.insert(tk.END, result_str)
        entry_result.config(state=tk.DISABLED)

# Tao giao dien
win = tk.Tk()
win.title("Nhan hai ma tran");
# win.geometry('400x400')

# Ma trận A
label_matrix_A = tk.Label(win, text="Ma trận A:")
label_matrix_A.grid(row=0, column=0, padx=10, pady=10)

entry_matrix_A = tk.Text(win, height=5, width=20)
entry_matrix_A.grid(row=1, column=0, padx=10, pady=10)

# Ma trận B
label_matrix_B = tk.Label(win, text="Ma trận B:")
label_matrix_B.grid(row=0, column=1, padx=10, pady=10)

entry_matrix_B = tk.Text(win, height=5, width=20)
entry_matrix_B.grid(row=1, column=1, padx=10, pady=10)

# Nút tính toán
btn_calculate = tk.Button(win, text="Tính toán", command=matrix_multiplication)
btn_calculate.grid(row=2, column=0, columnspan=2, pady=10)

# Kết quả
label_result = tk.Label(win, text="Kết quả:")
label_result.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

entry_result = tk.Text(win, height=5, width=40, state=tk.DISABLED)
entry_result.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

win.mainloop()