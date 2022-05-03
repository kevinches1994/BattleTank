import tkinter
from tkinter import Label #, PhotoImage
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

        menubar.add_command(label="Salir", command = self.destroy)
        menubar.add_command(label= "Reiniciar", command = self.__restart)
        
        self.config(menu=menubar)

        self.withdraw()

    def set_controller(self, controller):
        self.controller = controller

    def __restart(self):
        self.controller.restart()
        self.game_grid = self.controller.get_game_grid()
        self.create_logical_button_grid()

    def create_logical_button_grid(self):
        self.game_ui_grid = []
        for row_index in range(self.cols_number):
            row_label = []
            for col_index in range(self.cols_number):
                lbl = Label(self.mainFrame, borderwidth=0)
                self.put_image_label(lbl, self.game_grid, row_index, col_index)
                row_label.append(lbl)
                lbl.grid(row = row_index, column = col_index)
            self.game_ui_grid.append(row_label)

    def put_image_label(self, lbl, game_grid, row_index, column_index, action=None):

        image_path = None
        resize_tuple = (40, 40)

        if game_grid[row_index, column_index] == 0:
            image_path = 'images/queen.bmp'
        elif game_grid[row_index, column_index] == 1:
            image_path = 'images/player_right.bmp'
        elif game_grid[row_index, column_index] == 2:
            if action is None:
                action = 'LEFT'
            image_path = 'images/enemy_{}.bmp'.format(action.lower())
        elif game_grid[row_index, column_index] == 3:
            image_path = 'images/wall.bmp'
        elif game_grid[row_index, column_index] == 4:
            image_path = 'images/brick.bmp'
        elif game_grid[row_index, column_index] == 5:
            image_path = 'images/road.bmp'

        assert image_path is not None
        
        with Image.open(image_path) as cell_image:
            image = ImageTk.PhotoImage(cell_image.resize(resize_tuple))
            lbl.config(image=image)
            lbl.image = image


