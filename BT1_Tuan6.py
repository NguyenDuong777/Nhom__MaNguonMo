import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import numpy as np
import matplotlib.pyplot as plt

# Hàm để chọn ảnh
def choose_image():
    global img, img_path, img_display
    img_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
    if img_path:
        img = cv2.imread(img_path)
        img_display = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        display_image_in_label(img_display)
        messagebox.showinfo("Info", "Image selected successfully.")

# Hàm chụp ảnh từ camera
def capture_image():
    global img, img_display
    cap = cv2.VideoCapture(0)  # Mở camera
    if not cap.isOpened():
        messagebox.showwarning("Warning", "Could not open camera.")
        return

    ret, frame = cap.read()  # Đọc khung hình từ camera
    if ret:
        img = frame  # Lưu khung hình vào biến img
        img_display = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        display_image_in_label(img_display)
        messagebox.showinfo("Info", "Image captured successfully.")
    else:
        messagebox.showwarning("Warning", "Failed to capture image.")

    cap.release()  # Giải phóng camera

# Hàm hiển thị ảnh lên giao diện bên cạnh các nút
def display_image_in_label(image):
    image_pil = Image.fromarray(image)
    image_pil.thumbnail((300, 300))  # Thay đổi kích thước ảnh cho vừa với Label
    image_tk = ImageTk.PhotoImage(image_pil)
    image_label.config(image=image_tk)
    image_label.image = image_tk  # Lưu tham chiếu để tránh bị thu hồi bộ nhớ

# Hàm tăng độ nét
def sharpen_image():
    global sharpened
    if img is None:
        messagebox.showwarning("Warning", "Please select or capture an image first.")
        return

    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    sharpened = cv2.filter2D(img, -1, kernel)
    display_with_matplotlib(sharpened, "Sharpened")

# Hàm chuyển ảnh sang đen trắng
def grayscale_image():
    global gray
    if img is None:
        messagebox.showwarning("Warning", "Please select or capture an image first.")
        return

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    display_with_matplotlib(gray, "Grayscale", cmap='gray')

# Hàm giảm độ phân giải
def reduce_resolution_image():
    global reduced_resolution
    if img is None:
        messagebox.showwarning("Warning", "Please select or capture an image first.")
        return

    reduced_resolution = reduce_resolution(img)
    display_with_matplotlib(reduced_resolution, "Reduced Resolution")

# Hàm giảm độ phân giải của ảnh sử dụng fx và fy
def reduce_resolution(image, scale=0.1):
    reduced = cv2.resize(image, (0, 0), fx=scale, fy=scale)
    return reduced

# Hàm làm đẹp ảnh (xóa tàn nhang, mụn, làm mịn da)
def beauty_image():
    global beauty
    if img is None:
        messagebox.showwarning("Warning", "Please select or capture an image first.")
        return

    # Làm mịn da bằng cách áp dụng bộ lọc Bilateral Filter
    smooth = cv2.bilateralFilter(img, d=15, sigmaColor=75, sigmaSpace=75)

    # Chuyển ảnh gốc sang HSV để tách màu sắc
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Giảm độ sáng (vì một số khuyết điểm có thể sáng hơn màu da)
    h, s, v = cv2.split(img_hsv)
    v = cv2.subtract(v, 30)  # Giảm độ sáng
    img_hsv = cv2.merge((h, s, v))
    img_corrected = cv2.cvtColor(img_hsv, cv2.COLOR_HSV2BGR)

    # Kết hợp hình ảnh đã làm mịn với hình ảnh đã điều chỉnh màu sắc
    beauty = cv2.addWeighted(smooth, 0.7, img_corrected, 0.3, 0)

    # Hiển thị ảnh đã xử lý
    display_with_matplotlib(beauty, "Beauty")

# Hàm hiển thị ảnh bằng matplotlib
def display_with_matplotlib(image, title, cmap=None):
    plt.figure(figsize=(5, 5))
    if cmap:
        plt.imshow(image, cmap=cmap)
    else:
        plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.title(title)
    plt.axis('off')
    plt.show()

# Hàm để lưu tất cả ảnh đã xử lý
def save_image():
    if sharpened is None and gray is None and reduced_resolution is None and beauty is None:
        messagebox.showwarning("Warning", "Please apply at least one filter before saving.")
        return

    save_directory = filedialog.askdirectory(title="Select Directory to Save Images")
    if save_directory:
        # Lưu các ảnh đã xử lý
        if sharpened is not None:
            cv2.imwrite(f"{save_directory}/sharpened.png", sharpened)
        if gray is not None:
            cv2.imwrite(f"{save_directory}/grayscale.png", gray)
        if reduced_resolution is not None:
            cv2.imwrite(f"{save_directory}/reduced_resolution.png", reduced_resolution)
        if beauty is not None:
            cv2.imwrite(f"{save_directory}/beauty.png", beauty)
        messagebox.showinfo("Info", "Images saved successfully!")

# Khởi tạo giao diện
root = tk.Tk()
root.title("Image Filter Application")

# Tạo một frame để chứa các nút và hình ảnh
frame_controls = tk.Frame(root)
frame_controls.pack(side=tk.LEFT, padx=10, pady=10)

btn_choose = tk.Button(frame_controls, text="Choose Image", command=choose_image)
btn_choose.pack(pady=10)

btn_capture = tk.Button(frame_controls, text="Capture Image", command=capture_image)
btn_capture.pack(pady=10)

btn_sharpen = tk.Button(frame_controls, text="Sharpen Image", command=sharpen_image)
btn_sharpen.pack(pady=10)

btn_grayscale = tk.Button(frame_controls, text="Grayscale Image", command=grayscale_image)
btn_grayscale.pack(pady=10)

btn_reduce = tk.Button(frame_controls, text="Reduce Resolution", command=reduce_resolution_image)
btn_reduce.pack(pady=10)

btn_beauty = tk.Button(frame_controls, text="Beauty", command=beauty_image)
btn_beauty.pack(pady=10)

btn_save = tk.Button(frame_controls, text="Save Images", command=save_image)
btn_save.pack(pady=10)

btn_exit = tk.Button(frame_controls, text="Exit", command=root.quit)
btn_exit.pack(pady=10)

# Tạo Label để hiển thị ảnh gốc
image_label = tk.Label(root)
image_label.pack(side=tk.RIGHT, padx=10, pady=10)

img = None
img_path = ""
img_display = None
sharpened = None
gray = None
reduced_resolution = None
beauty = None

root.mainloop()
