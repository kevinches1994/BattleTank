import tkinter as tk
from tkinter import *
from PIL import ImageTk ,Image

root = tk.Tk()
LeftFrame = tk.Frame(root)
LeftFrame.grid()

def checker(i,j):
    print(f"You pressed button {i},{j}")

#Create a 2-d list containing 3 rows, 3 columns (using list comprehension)
botones = [[None for i in range(3)] for j in range(3) ]

for i in range(3):
    for j in range(3):
        """
        current_button = tk.Button(LeftFrame,
                               text = f"{i},{j}",
                               font=("tahoma", 25, "bold"),
                               height = 3,
                               width = 8,
                               bg="gainsboro",
                               compound = LEFT,
                               image = PhotoImage(file = "images/brick.png"),
                               command=lambda i=i,j=j:checker(i,j)) #lambda is passed parameters i and j
        """
        img = ImageTk.PhotoImage(Image.open('images/brick.bmp').resize((10, 10))) # the one-liner I used in my app
        current_button = Label(LeftFrame, image=img, borderwidth=1)
        current_button.image = img
        #Grid occurs on a new line
        current_button.grid(row = i+1, column = j+1)
        botones[i][j] = current_button

root.mainloop()