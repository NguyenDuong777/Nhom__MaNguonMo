import tkinter as tk
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

        # Hiển thị kết quả trực tiếp trên giao diện
        solution_str = "\n".join([f"x{i + 1} = {solutions[i]:.2f}" for i in range(n)])
        label_solution.config(text=solution_str)

    except ValueError:
        messagebox.showerror("Lỗi", "Vui lòng đảm bảo rằng tất cả các ô nhập chứa số hợp lệ.")
    except np.linalg.LinAlgError:
        messagebox.showerror("Lỗi", "Hệ phương trình không có nghiệm duy nhất.")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {str(e)}")

# Hàm để xóa các ô nhập liệu
def clear_entries():
    try:
        for row in coefficient_entries:
            for entry in row:
                entry.delete(0, tk.END)
        for entry in result_entries:
            entry.delete(0, tk.END)
        label_solution.config(text="")  # Xóa kết quả
    except Exception as e:
        messagebox.showerror("Lỗi", "Không thể xóa dữ liệu. Hãy chắc chắn rằng các ô nhập đã được tạo.")

# Hàm để tạo các ô nhập hệ số và kết quả
def create_entries():
    global coefficient_entries, result_entries
    try:
        n = int(entry_n.get())
        if n <= 0:
            messagebox.showerror("Lỗi", "Hãy nhập một số nguyên dương cho n.")
            return
        
        # Xóa các ô nhập cũ nếu có
        for widget in frame_entries.winfo_children():
            widget.destroy()

        coefficient_entries = []
        result_entries = []

        # Tạo các ô nhập liệu cho ma trận hệ số
        for i in range(n):
            row_entries = []
            for j in range(n):
                entry = tk.Entry(frame_entries, width=5)
                entry.grid(row=i, column=j, padx=2, pady=2)
                row_entries.append(entry)
            coefficient_entries.append(row_entries)

        # Tạo các ô nhập cho kết quả
        for i in range(n):
            entry = tk.Entry(frame_entries, width=5)
            entry.grid(row=i, column=n + 1, padx=2, pady=2)
            result_entries.append(entry)

        label_solution.config(text="")  # Xóa kết quả cũ
    except ValueError:
        messagebox.showerror("Lỗi", "Hãy nhập một số nguyên hợp lệ cho n.")

# Giao diện người dùng bằng Tkinter
root = tk.Tk()
root.title("Giải hệ n phương trình n ẩn")
root.geometry("600x400")

# Nhập số n
label_n = tk.Label(root, text="Nhập số ẩn n:")
label_n.grid(row=0, column=0, padx=10, pady=10)
entry_n = tk.Entry(root)
entry_n.grid(row=0, column=1, padx=10, pady=10)

# Nút tạo các ô nhập
button_create_entries = tk.Button(root, text="Tạo các ô nhập", command=create_entries)
button_create_entries.grid(row=0, column=2, padx=10, pady=10)

# Khung chứa các ô nhập hệ số và kết quả
frame_entries = tk.Frame(root)
frame_entries.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

# Nút giải phương trình
button_solve = tk.Button(root, text="Giải phương trình", command=solve_equations)
button_solve.grid(row=2, column=0, padx=10, pady=10)

# Nút xóa dữ liệu
button_clear = tk.Button(root, text="Xóa dữ liệu", command=clear_entries)
button_clear.grid(row=2, column=1, padx=10, pady=10)

# Nhãn hiển thị kết quả
label_solution = tk.Label(root, text="", fg="blue", font=("Arial", 12))
label_solution.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

root.mainloop()
