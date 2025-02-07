import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageOps, ImageEnhance

class ImageEditor:
    def __init__(self, root):
         # Initialize the main window
        self.root = root
        self.root.title("Image Editor")
        self.root.geometry("1200x800")
        self.root.configure(bg="#2D2D2D")
        
        # Initialize variables to store images and states
        self.image = None # Original loaded image
        self.cropped_image = None # Cropped portion of the image
        self.tk_image = None # Tkinter-compatible image for display
        self.rect_id = None # ID of the rectangle drawn on the canvas
        self.start_x = self.start_y = None # Starting coordinates for cropping
        self.end_x = self.end_y = None # Ending coordinates for cropping
        self.modified_image = None # Image after applying modifications
        self.undo_stack = [] # Stack to keep track of changes for undo
        self.redo_stack = [] # Stack to keep track of changes for redo
        self.is_grayscale = False # Flag to check if the image is grayscale
        self.original_image = None # Original image before modifications
        
        # Main Frame
        self.main_frame = tk.Frame(root, bg="#2D2D2D")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Left Panel for Image Display
        self.left_panel = tk.Frame(self.main_frame, bg="#3C3C3C", bd=2, relief=tk.RAISED)
        self.left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Canvas for Image
        self.canvas = tk.Canvas(self.left_panel, bg="#3C3C3C", width=800, height=600, highlightthickness=0)
        self.canvas.pack(pady=20)
        self.canvas.bind("<ButtonPress-1>", self.on_press) # Bind mouse press event
        self.canvas.bind("<B1-Motion>", self.on_drag) # Bind mouse drag event
        self.canvas.bind("<ButtonRelease-1>", self.on_release) # Bind mouse release event
        
        # Right Panel for Controls
        self.right_panel = tk.Frame(self.main_frame, bg="#252526", bd=2, relief=tk.RAISED)
        self.right_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)
        
        # Load Image Button
        self.load_button = tk.Button(self.right_panel, text="Load Image", command=self.load_image, bg="#007ACC", fg="white", font=("Arial", 12, "bold"), width=20, bd=0, relief=tk.FLAT)
        self.load_button.pack(pady=10)
        
        # Cropped Image Display
        self.cropped_canvas = tk.Canvas(self.right_panel, bg="#3C3C3C", width=200, height=200, highlightthickness=0)
        self.cropped_canvas.pack(pady=20)
        
       
    
    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.png;*.jpeg;*.bmp;*.tiff")])
        if not file_path:
            return
        
        try:
            self.image = cv2.imread(file_path)
            if self.image is None:
                messagebox.showerror("Error", "Unsupported image format or corrupted file!")
                return
            self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            self.image = self.resize_to_fit(self.image, 800, 600)
            self.display_image(self.image)
            self.undo_stack = []
            self.redo_stack = []
            self.is_grayscale = False
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image: {str(e)}")
    
    def resize_to_fit(self, img, frame_width, frame_height):
        h, w = img.shape[:2]
        scale = min(frame_width / w, frame_height / h)
        new_w, new_h = int(w * scale), int(h * scale)
        return cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)
    
    def display_image(self, img):
        self.canvas.delete("all")
        img = Image.fromarray(img)
        self.tk_image = ImageTk.PhotoImage(img)
        self.canvas.create_image(400, 300, anchor=tk.CENTER, image=self.tk_image)
    
    def display_cropped_image(self, img):
        self.cropped_canvas.delete("all")
        img = Image.fromarray(img)
        img.thumbnail((200, 200))
        self.tk_cropped_image = ImageTk.PhotoImage(img)
        self.cropped_canvas.create_image(100, 100, anchor=tk.CENTER, image=self.tk_cropped_image)
    
    def on_press(self, event):
        self.canvas.delete("rect")
        self.start_x, self.start_y = event.x, event.y
        self.rect_id = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline="red", tags="rect")
    
    def on_drag(self, event):
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        end_x = max(0, min(event.x, canvas_width))
        end_y = max(0, min(event.y, canvas_height))
        
        self.canvas.coords(self.rect_id, self.start_x, self.start_y, end_x, end_y)
    
    def on_release(self, event):
        self.end_x, self.end_y = event.x, event.y
        if None in (self.start_x, self.start_y, self.end_x, self.end_y):
            return
        if self.image is not None:
            x1, x2 = sorted([self.start_x, self.end_x])
            y1, y2 = sorted([self.start_y, self.end_y])
            if x1 < x2 and y1 < y2:
                h, w = self.image.shape[:2]
                canvas_width = self.canvas.winfo_width()
                canvas_height = self.canvas.winfo_height()
                scale_x = w / canvas_width
                scale_y = h / canvas_height
                
                x1_scaled = int(x1 * scale_x)
                y1_scaled = int(y1 * scale_y)
                x2_scaled = int(x2 * scale_x)
                y2_scaled = int(y2 * scale_y)
                
                self.cropped_image = self.image[y1_scaled:y2_scaled, x1_scaled:x2_scaled]
                self.modified_image = self.cropped_image
                self.original_image = self.cropped_image.copy()
                self.display_cropped_image(self.cropped_image)
                self.resize_slider.set(100)
                self.push_to_undo_stack(self.cropped_image)
                self.is_grayscale = False
                self.brightness_slider.set(1.0)
    
    def resize_cropped_image(self, scale):
        if self.modified_image is None:
            return
        scale = int(scale) / 100.0
        resized_image = cv2.resize(self.modified_image, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
        self.display_cropped_image(resized_image)
    
    def toggle_grayscale(self):
        if self.modified_image is None:
            return
        
        if not self.is_grayscale:
            self.original_image = self.modified_image.copy()
            gray_image = cv2.cvtColor(self.modified_image, cv2.COLOR_RGB2GRAY)
            self.modified_image = cv2.cvtColor(gray_image, cv2.COLOR_GRAY2RGB)
            self.is_grayscale = True
        else:
            self.modified_image = self.original_image.copy()
            self.is_grayscale = False
        
        self.display_cropped_image(self.modified_image)
        self.push_to_undo_stack(self.modified_image)
    
    def adjust_brightness(self, value):
        if self.modified_image is None or self.original_image is None:
            return
        
        brightness_factor = float(value)
        pil_image = Image.fromarray(self.original_image)
        enhancer = ImageEnhance.Brightness(pil_image)
        bright_image = enhancer.enhance(brightness_factor)
        self.modified_image = np.array(bright_image)
        self.display_cropped_image(self.modified_image)
    
    def rotate_image(self):
        if self.modified_image is None:
            return
        rotated_image = cv2.rotate(self.modified_image, cv2.ROTATE_90_CLOCKWISE)
        self.modified_image = rotated_image
        self.display_cropped_image(self.modified_image)
        self.push_to_undo_stack(self.modified_image)
    
    def save_image(self):
        if self.modified_image is None:
            messagebox.showerror("Error", "No image to save!")
            return
        
        save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG file", "*.png"), ("JPEG file", "*.jpg")])
        if save_path:
            save_img = Image.fromarray(self.modified_image)
            save_img.save(save_path)
            messagebox.showinfo("Success", "Image saved successfully!")
    
    def push_to_undo_stack(self, image):
        self.undo_stack.append(image.copy())
        self.redo_stack = []
    
    def undo(self):
        if len(self.undo_stack) > 1:
            self.redo_stack.append(self.undo_stack.pop())
            self.modified_image = self.undo_stack[-1].copy()
            self.display_cropped_image(self.modified_image)
        elif len(self.undo_stack) == 1:
            self.redo_stack.append(self.undo_stack.pop())
            self.modified_image = None
            self.cropped_canvas.delete("all")
    
    def redo(self):
        if self.redo_stack:
            self.undo_stack.append(self.redo_stack.pop())
            self.modified_image = self.undo_stack[-1].copy()
            self.display_cropped_image(self.modified_image)

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEditor(root)
    root.mainloop()