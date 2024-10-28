import cv2
import numpy as np
from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

class ImageProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Processing Application")
        
        self.img_original = None
        self.img_display = None
        
        # Create UI components
        self.create_widgets()
        
    def create_widgets(self):
        # Frames for layout organization
        self.panelA = Label(self.root)  # Frame to display original image
        self.panelA.grid(row=0, column=0, padx=10, pady=10)
        
        self.panelB = Label(self.root)  # Frame to display processed image
        self.panelB.grid(row=0, column=1, padx=10, pady=10)
        
        # Buttons for image operations
        Button(self.root, text="Select Image", command=self.select_image).grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        Button(self.root, text="Open Camera", command=self.open_camera).grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        
        Button(self.root, text="Blur", command=self.apply_blur).grid(row=2, column=0, padx=10, pady=5, sticky="ew")
        Button(self.root, text="Sharpen", command=self.apply_sharpen).grid(row=2, column=1, padx=10, pady=5, sticky="ew")
        
        Button(self.root, text="Grayscale", command=self.apply_grayscale).grid(row=3, column=0, padx=10, pady=5, sticky="ew")
        Button(self.root, text="Remove Freckles", command=self.remove_freckles).grid(row=3, column=1, padx=10, pady=5, sticky="ew")
        
        Button(self.root, text="Blur Background", command=self.blur_background).grid(row=4, column=0, padx=10, pady=5, sticky="ew")
        Button(self.root, text="Save Image", command=self.save_image).grid(row=4, column=1, padx=10, pady=5, sticky="ew")

    def select_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.img_original = cv2.imread(file_path)
            self.img_display = self.img_original.copy()
            self.show_image(self.img_original, self.img_display)

    def open_camera(self):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            messagebox.showerror("Camera Error", "Unable to open the camera.")
            return

        ret, frame = cap.read()
        if ret:
            self.img_original = frame.copy()
            self.img_display = frame.copy()
            self.show_image(self.img_original, self.img_display)
        cap.release()
        cv2.destroyAllWindows()

    def show_image(self, original, processed):
        image_rgb_original = cv2.cvtColor(original, cv2.COLOR_BGR2RGB)
        image_pil_original = Image.fromarray(image_rgb_original)
        image_tk_original = ImageTk.PhotoImage(image_pil_original)
        self.panelA.config(image=image_tk_original)
        self.panelA.image = image_tk_original
        
        # Display processed image
        image_rgb_processed = cv2.cvtColor(processed, cv2.COLOR_BGR2RGB)
        image_pil_processed = Image.fromarray(image_rgb_processed)
        image_tk_processed = ImageTk.PhotoImage(image_pil_processed)
        self.panelB.config(image=image_tk_processed)
        self.panelB.image = image_tk_processed

    def apply_blur(self):
        if self.img_display is not None:
            blurred = cv2.GaussianBlur(self.img_display, (15, 15), 0)
            self.show_image(self.img_original, blurred)

    def apply_sharpen(self):
        if self.img_display is not None:
            kernel_sharpening = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
            sharpened = cv2.filter2D(self.img_display, -1, kernel_sharpening)
            self.show_image(self.img_original, sharpened)

    def apply_grayscale(self):
        if self.img_display is not None:
            gray = cv2.cvtColor(self.img_display, cv2.COLOR_BGR2GRAY)
            gray_bgr = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
            self.show_image(self.img_original, gray_bgr)

    def remove_freckles(self):
        if self.img_display is not None:
            smoothed = cv2.bilateralFilter(self.img_display, 9, 75, 75)
            self.show_image(self.img_original, smoothed)

    def blur_background(self):
        if self.img_display is not None:
            mask = np.zeros(self.img_display.shape[:2], np.uint8)
            bgdModel = np.zeros((1, 65), np.float64)
            fgdModel = np.zeros((1, 65), np.float64)
            rect = (50, 50, self.img_display.shape[1] - 50, self.img_display.shape[0] - 50)
            cv2.grabCut(self.img_display, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)
            mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
            img = self.img_display * mask2[:, :, np.newaxis]
            blurred_bg = cv2.GaussianBlur(self.img_display, (21, 21), 0)
            img_with_blurred_bg = np.where(mask2[:, :, None] == 1, self.img_display, blurred_bg)
            self.show_image(self.img_original, img_with_blurred_bg)

    def save_image(self):
        if self.img_display is not None:
            file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                     filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
            if file_path:
                cv2.imwrite(file_path, self.img_display)

root = Tk()
app = ImageProcessorApp(root)
root.mainloop()
