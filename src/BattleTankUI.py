import tkinter
from tkinter import Label, Frame, TOP, LEFT, BOTTOM  #, PhotoImage
from tkinter.messagebox import askyesno
from PIL import ImageTk ,Image

class BattleTankUI(tkinter.Tk):

    def __init__(self, cols_number, rows_number, game_grid):

        tkinter.Tk.__init__(self)

        self.title("Battle Tank")

        # variables que definen filas y columnas
        self.cols_number = cols_number

        self.rows_number = rows_number

        self.mainFrame = tkinter.Frame(self)

        self.__shape = (441, 459)
        self.__width, self.__height = self.__shape
        self.minsize(self.__width, self.__height)
        self.maxsize(self.__width, self.__height)
        
        self.__topframe = Frame(self)
        self.__topframe.pack(side = TOP, fill = "x", expand = False) 

        redbutton = Label(self.__topframe, text = "Red", fg = "red", borderwidth = 1) 
        redbutton.pack(side = LEFT, fill = "both", expand = True) 
        
        greenbutton = Label(self.__topframe, text = "Brown", fg = "brown", borderwidth = 1) 
        greenbutton.pack(side = LEFT, fill = "both", expand = True) 
        
        bluebutton = Label(self.__topframe, text = "Blue", fg = "blue", borderwidth = 1) 
        bluebutton.pack(side = LEFT, fill = "both", expand = True)

        self.__gridframe = Frame(self)
        self.__gridframe.pack(side = BOTTOM, fill = "both", expand = True)

        # llama a la funcion que crea los botones

        self.__create_logical_button_grid(game_grid)
        
        menubar = tkinter.Menu(self)

        menubar.add_command(label="Salir", command = self.destroy)
        menubar.add_command(label= "Reiniciar", command = self.__confirm_restart)
        
        self.config(menu=menubar)

        gameAlgorithmsMenu = tkinter.Menu(menubar)
        gameAlgorithmsMenu.add_command(label="Usando simulated annealing", command = self.__play_with_simulated_annealing)
        menubar.add_cascade(label="Jugar", menu=gameAlgorithmsMenu)

        #self.withdraw()

    def __play_with_simulated_annealing(self):
        print("Playing with using simulated annealing")
        self.__controller.play_simulated_annealing()
        answer = askyesno(title='Confirmación',
                    message='¿Esta seguro que desea jugar?')
        if answer:
            self.__controller.confirm_play()

    def set_controller(self, controller):
        self.__controller = controller

    def __confirm_restart(self):
        answer = askyesno(title='Confirmación',
                    message='¿Esta seguro que desea reiniciar?')
        if answer:
            self.__controller.restart()
            self.__repaint_logical_button_grid(self.__controller.get_game_grid())

    def __create_logical_button_grid_old(self, game_grid):
        self.game_ui_grid = []
        for row_index in range(self.cols_number):
            row_label = []
            for col_index in range(self.cols_number):
                lbl = Label(self.mainFrame, borderwidth=0)
                self.__put_image_label(lbl, game_grid, row_index, col_index)
                row_label.append(lbl)
                lbl.grid(row = row_index, column = col_index)
            self.game_ui_grid.append(row_label)

    def __create_logical_button_grid(self, game_grid):

        self.game_ui_grid = []
        for row_index in range(self.cols_number):

            row_label = []
            rowgridframe = Frame(self.__gridframe)
            rowgridframe.pack(side = TOP, fill = "both", expand = True)

            for col_index in range(self.cols_number):
                lbl = Label(rowgridframe, borderwidth = 0)
                self.__put_image_label(lbl, game_grid, row_index, col_index)
                row_label.append(lbl)
                lbl.pack(side = LEFT, fill = "both", expand = True, ipadx = 0, ipady = 0, padx = 0, pady = 0)

            self.game_ui_grid.append(row_label)

    def __repaint_logical_button_grid(self, game_grid):
        for row_index in range(len(game_grid)):
            for col_index in range(len(game_grid[0])):
                self.update_image_cell(game_grid, row_index, col_index)

    def __put_image_label(self, lbl, game_grid, row_index, column_index, action=None):

        image_path = None
        resize_tuple = (40, 40)

        if game_grid[row_index, column_index] == 0:
            image_path = 'images/queen.bmp'
        elif game_grid[row_index, column_index] == 1:
            if action is None:
                action = 'RIGHT'    
            image_path = 'images/player_{}.bmp'.format(action.lower())
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

    def update_image_cell(self, game_grid, row_index, col_index, action = None):
        lbl = self.game_ui_grid[row_index][col_index]
        self.__put_image_label(lbl, game_grid, row_index, col_index, action)


