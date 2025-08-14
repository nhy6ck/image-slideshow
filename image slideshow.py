import os
import tkinter as tk
from PIL import Image, ImageTk
import itertools

folder = 'img'
image_files = [f for f in os.listdir(folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
image_cycle = itertools.cycle(image_files)

root = tk.Tk()
root.title("Image Slideshow")

window_width = 600
window_height = 400

def center_window(win, width, height):
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    win.geometry(f"{width}x{height}+{x}+{y}")

center_window(root, window_width, window_height)
root.resizable(True, True)

label = tk.Label(root)
label.pack(expand=True, fill=tk.BOTH)

current_image_pil = None
photo = None

def fit_image_to_window(image, window_size):
    image_width, image_height = image.size
    window_width, window_height = window_size
    if window_width <= 0 or window_height <= 0:
        return image
    
    aspect_ratio = image_width / image_height
    
    if (window_width / window_height) > aspect_ratio:
        new_height = window_height
        new_width = int(new_height * aspect_ratio)
    else:
        new_width = window_width
        new_height = int(new_width / aspect_ratio)
    
    if new_width <= 0:
        new_width = 1
    if new_height <= 0:
        new_height = 1

    resized = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    return resized

def update_image():
    global current_image_pil, photo
    image_file = next(image_cycle)
    current_image_pil = Image.open(os.path.join(folder, image_file))
    
    w = root.winfo_width()
    h = root.winfo_height()
    
    resized = fit_image_to_window(current_image_pil, (w, h))
    photo = ImageTk.PhotoImage(resized)
    label.config(image=photo)
    label.image = photo
    
    root.after(3000, update_image)

def resize_image(event):
    global photo
    if current_image_pil and event.widget == root:
        w, h = event.width, event.height
        resized = fit_image_to_window(current_image_pil, (w, h))
        photo = ImageTk.PhotoImage(resized)
        label.config(image=photo)
        label.image = photo

root.bind("<Configure>", resize_image)

update_image()
root.mainloop()