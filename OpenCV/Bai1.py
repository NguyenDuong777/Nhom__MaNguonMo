import cv2
import numpy as np
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk

# Khai báo biến cho ảnh gốc và ảnh đã chỉnh sửa
img_original = None
img_display = None


# Các bộ lọc cơ bản
def apply_blur():
    global img_display
    blurred = cv2.GaussianBlur(img_display, (15, 15), 0)
    show_image(img_original, blurred)


def apply_sharpen():
    global img_display
    kernel_sharpening = np.array([[-1, -1, -1],
                                  [-1, 9, -1],
                                  [-1, -1, -1]])
    sharpened = cv2.filter2D(img_display, -1, kernel_sharpening)
    show_image(img_original, sharpened)


def apply_grayscale():
    global img_display
    gray = cv2.cvtColor(img_display, cv2.COLOR_BGR2GRAY)
    show_image(img_original, gray)


# Chức năng xóa tàn nhang
def remove_freckles():
    global img_display
    smoothed = cv2.bilateralFilter(img_display, 9, 75, 75)
    show_image(img_original, smoothed)


# Chức năng xóa phông
def blur_background():
    global img_display
    mask = np.zeros(img_display.shape[:2], np.uint8)
    bgdModel = np.zeros((1, 65), np.float64)
    fgdModel = np.zeros((1, 65), np.float64)

    # Hình chữ nhật đại diện cho đối tượng cần giữ lại (foreground)
    rect = (50, 50, img_display.shape[1] - 50, img_display.shape[0] - 50)

    cv2.grabCut(img_display, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)
    mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
    img = img_display * mask2[:, :, np.newaxis]

    # Làm mờ nền
    blurred_bg = cv2.GaussianBlur(img_display, (21, 21), 0)
    img_with_blurred_bg = np.where(mask2[:, :, None] == 1, img_display, blurred_bg)

    show_image(img_original, img_with_blurred_bg)


# Chọn ảnh từ máy tính
def select_image():
    global img_original, img_display
    file_path = filedialog.askopenfilename()
    if file_path:
        img_original = cv2.imread(file_path)
        img_display = img_original.copy()  # Bản sao để hiển thị
        show_image(img_original, img_display)


# Chụp ảnh từ camera
def open_camera():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if ret:
            cv2.imshow('Camera', frame)
            if cv2.waitKey(1) == ord('o'):
                cv2.imwrite('temp.png', frame)
                img = cv2.imread('temp.png')
                global img_original, img_display
                img_original = img.copy()  # Ảnh gốc
                img_display = img.copy()  # Bản sao để hiển thị
                show_image(img_original, img_display)
                break
        else:
            break
    cap.release()
    cv2.destroyAllWindows()


# Hiển thị ảnh trong giao diện
def show_image(original, processed):
    # Hiển thị ảnh gốc
    image_rgb_original = cv2.cvtColor(original, cv2.COLOR_BGR2RGB)
    image_pil_original = Image.fromarray(image_rgb_original)
    image_tk_original = ImageTk.PhotoImage(image_pil_original)
    panelA.config(image=image_tk_original)
    panelA.image = image_tk_original

    # Hiển thị ảnh đã chỉnh sửa
    image_rgb_processed = cv2.cvtColor(processed, cv2.COLOR_BGR2RGB)
    image_pil_processed = Image.fromarray(image_rgb_processed)
    image_tk_processed = ImageTk.PhotoImage(image_pil_processed)
    panelB.config(image=image_tk_processed)
    panelB.image = image_tk_processed


# Lưu ảnh đã chỉnh sửa
def save_image():
    file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                             filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
    if file_path:
        cv2.imwrite(file_path, img_display)


# Giao diện Tkinter
root = Tk()
root.title("Image Processing Application")

# Khung chứa ảnh gốc và ảnh chỉnh sửa
panelA = Label(root)  # Khung hiển thị ảnh gốc
panelA.pack(side="left", padx=10, pady=10)

panelB = Label(root)  # Khung hiển thị ảnh đã chỉnh sửa
panelB.pack(side="right", padx=10, pady=10)

# Nút chức năng
btn_select_image = Button(root, text="Select Image", command=select_image)
btn_select_image.pack(side="top", fill="both", expand="yes", padx=10, pady=5)

btn_camera = Button(root, text="Open Camera", command=open_camera)
btn_camera.pack(side="top", fill="both", expand="yes", padx=10, pady=5)

btn_blur = Button(root, text="Blur", command=apply_blur)
btn_blur.pack(side="top", fill="both", expand="yes", padx=10, pady=5)

btn_sharpen = Button(root, text="Sharpen", command=apply_sharpen)
btn_sharpen.pack(side="top", fill="both", expand="yes", padx=10, pady=5)

btn_grayscale = Button(root, text="Grayscale", command=apply_grayscale)
btn_grayscale.pack(side="top", fill="both", expand="yes", padx=10, pady=5)

btn_freckles = Button(root, text="Remove Freckles", command=remove_freckles)
btn_freckles.pack(side="top", fill="both", expand="yes", padx=10, pady=5)

btn_blur_bg = Button(root, text="Blur Background", command=blur_background)
btn_blur_bg.pack(side="top", fill="both", expand="yes", padx=10, pady=5)

btn_save = Button(root, text="Save Image", command=save_image)
btn_save.pack(side="top", fill="both", expand="yes", padx=10, pady=5)

root.mainloop()
