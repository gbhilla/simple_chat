from tkinter import *
from PIL import ImageTk, Image

# Create the Tkinter window
window = Tk()

# Set the title of the window
window.title("Image Display")

# Open the image file
image = Image.open("C:/Users/hilla goren barnea/Pictures/flower.jpg")

# Resize the image if needed
# image = image.resize((width, height))

# Create an ImageTk object
img_tk = ImageTk.PhotoImage(image)

# Create a Label widget to display the image
label = Label(window, image=img_tk)

# Pack the Label widget to show it in the window
label.pack()

# Run the Tkinter event loop
window.mainloop()