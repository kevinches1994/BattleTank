import tkinter
from tkinter import Toplevel, Label, Button#, PhotoImage
from PIL import ImageTk ,Image

class BattleTankUI(tkinter.Tk):

    def __init__(self, cols_number, rows_number, game_grid):

        tkinter.Tk.__init__(self)

        self.title("Battle Tank")

        # variables que definen filas y columnas
        self.cols_number = cols_number

        self.rows_number = rows_number

        self.game_grid = game_grid

        self.mainFrame = tkinter.Frame(self)

        self.minsize(450,450)
        #(625,660)

        self.maxsize(600,600)
        #(625,660)
        
        self.mainFrame.grid()

        # llama a la funcion que crea los botones

        self.create_logical_button_grid()
        
        menubar = tkinter.Menu(self)

        menubar.add_command(label="Salir",command = self.destroy)
        menubar.add_command(label="Ocultar",command = self.withdraw)
        menubar.add_command(label= "Guardar",command = self.destroy)
        
        self.config(menu=menubar)

        self.withdraw()

    def create_logical_button_grid(self):
        self.game_ui_grid = []
        for row_index in range(self.cols_number):
            row_label = []
            for col_index in range(self.cols_number):
                """
                btn = tkinter.Button(self.mainFrame,text="",bg="white",
                                     width=5,height =1,fg="white",
                                     command = self.say_hi)
                """
                lbl = Label(self.mainFrame, borderwidth=0)
                self.put_image_label(lbl, row_index, col_index)
                row_label.append(lbl)
                lbl.grid(row = row_index, column = col_index)
            self.game_ui_grid.append(row_label)

    def put_image_label(self, lbl, row_index, column_index):

        image = None
        resize_tuple = (40, 40)
        
        if self.game_grid[row_index, column_index] == 0:
            image = Image.open('images/queen.bmp')
        elif self.game_grid[row_index, column_index] == 1:
            image = Image.open('images/player_right.bmp')
        elif self.game_grid[row_index, column_index] == 2:
            image = Image.open('images/enemy_left.bmp')
        elif self.game_grid[row_index, column_index] == 3:
            image = Image.open('images/wall.bmp')
        elif self.game_grid[row_index, column_index] == 4:
            image = Image.open('images/brick.bmp')
        else:
            image = Image.open('images/road.bmp')

        assert image is not None
        image = ImageTk.PhotoImage(image.resize(resize_tuple))
        lbl.config(image=image)
        lbl.image = image
        #btn.grid(row = row_index, column = column_index)

    def say_hi(self):
        root= Toplevel()
        root.title("Hi")
        root.geometry("450x450")
        Button(root, text= "Salir", command= root.destroy).pack()
        root.mainloop()



