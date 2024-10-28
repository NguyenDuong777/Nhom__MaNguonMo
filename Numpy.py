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
            messagebox.showerror("Error", "Kích thước không tương thích để nhân ma trận!")
            return None

        result = np.dot(A, B)
        display_result(result)

def matrix_addition():
    A = get_matrix_from_input(entry_matrix_A.get("1.0", tk.END))
    B = get_matrix_from_input(entry_matrix_B.get("1.0", tk.END))
    if A is not None and B is not None:
        if A.shape != B.shape:
            messagebox.showerror("Error", "Kích thước không tương thích để cộng ma trận!")
            return None

        result = A + B
        display_result(result)

def matrix_inversion():
    A = get_matrix_from_input(entry_matrix_A.get("1.0", tk.END))
    B = get_matrix_from_input(entry_matrix_B.get("1.0", tk.END))
    results = []
    
    if A is not None:
        if A.shape[0] == A.shape[1]:
            try:
                A_inv = np.linalg.inv(A)
                results.append("Nghịch đảo của ma trận A:\n" + matrix_to_string(A_inv))
            except np.linalg.LinAlgError:
                results.append("Ma trận A không có nghịch đảo.")
        else:
            results.append("Ma trận A không vuông, không thể tính nghịch đảo.")

    if B is not None:
        if B.shape[0] == B.shape[1]:
            try:
                B_inv = np.linalg.inv(B)
                results.append("Nghịch đảo của ma trận B:\n" + matrix_to_string(B_inv))
            except np.linalg.LinAlgError:
                results.append("Ma trận B không có nghịch đảo.")
        else:
            results.append("Ma trận B không vuông, không thể tính nghịch đảo.")
    
    display_result("\n\n".join(results))

def matrix_to_string(matrix):
    return "\n".join(["\t".join(map(lambda x: f"{x:.2f}", row)) for row in matrix])

def display_result(result):
    entry_result.config(state=tk.NORMAL)
    entry_result.delete("1.0", tk.END)
    if isinstance(result, str):
        entry_result.insert(tk.END, result)
    else:
        result_str = "\n".join(["\t".join(map(str, row)) for row in result])
        entry_result.insert(tk.END, result_str)
    entry_result.config(state=tk.DISABLED)

win = tk.Tk()
win.title("Tính toán ma trận")

# Matrix A
label_matrix_A = tk.Label(win, text="Matrix A:")
label_matrix_A.grid(row=0, column=0, padx=10, pady=10)

entry_matrix_A = tk.Text(win, height=5, width=20)
entry_matrix_A.grid(row=1, column=0, padx=10, pady=10)

# Matrix B
label_matrix_B = tk.Label(win, text="Matrix B:")
label_matrix_B.grid(row=0, column=1, padx=10, pady=10)

entry_matrix_B = tk.Text(win, height=5, width=20)
entry_matrix_B.grid(row=1, column=1, padx=10, pady=10)

# Buttons for operations
btn_calculate = tk.Button(win, text="Multiply Matrices", command=matrix_multiplication)
btn_calculate.grid(row=2, column=0, columnspan=2, pady=5)

btn_addition = tk.Button(win, text="Add Matrices", command=matrix_addition)
btn_addition.grid(row=3, column=0, columnspan=2, pady=5)

btn_inversion = tk.Button(win, text="Invert Matrices", command=matrix_inversion)
btn_inversion.grid(row=4, column=0, columnspan=2, pady=5)

# Result display
label_result = tk.Label(win, text="Result:")
label_result.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

entry_result = tk.Text(win, height=10, width=40, state=tk.DISABLED)
entry_result.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

win.mainloop()
