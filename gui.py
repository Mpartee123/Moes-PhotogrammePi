from tkinter import *
from PIL import ImageTk,Image

root = Tk()
root.title("Moe's PhotogrammePi")


#Define preview pane in Root
frame=LabelFrame(root, text="Preview Pane", padx=50, pady=50)
#Create Preview Pane in root
frame.pack(padx=10, pady=10)

#Create Image
img = ImageTk.PhotoImage(Image.open('images/download.jpeg'))
#define location and pane for image
label = Label(frame, image=img)
#Create image location
label.pack()

root.mainloop()
