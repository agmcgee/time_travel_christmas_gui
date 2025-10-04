import tkinter as tk
from PIL import Image, ImageTk

root = tk.Tk()
root.title("Image Display Example")

# Load the image using Pillow (for formats like JPG, PNG)
image = Image.open("lime-green.png")
photo = ImageTk.PhotoImage(image)

label = tk.Label(root, image=photo)
label.image = photo  # Keep a reference!
label.pack()

root.mainloop()