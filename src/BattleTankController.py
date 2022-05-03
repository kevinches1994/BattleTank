class BattleTankController():

    def __init__(self, problem, gameUI):
        self.problem = problem
        self.gameUI = gameUI
        self.__do_bindings()

    def show(self):
        self.gameUI.deiconify()

    def hide(self):
        self.gameUI.withdraw()

    def __left_key_pressed_event(self, event):
        print("Left key was pressed")

    def __right_key_pressed_event(self, event):
        print("Right key was pressed")

    def __up_key_pressed_event(self, event):
        print("Up key was pressed")

    def __down_key_pressed_event(self, event):
        print("Down key was pressed")        

    def __do_bindings(self):
        #self.gameUI.bind("<Key>", self.__key_pressed)
        #self.gameUI.bind("<Key>", lambda event: print("Key {} was pressed".format(event)))
        self.gameUI.bind("<Left>", self.__left_key_pressed_event)
        self.gameUI.bind("<Right>", self.__right_key_pressed_event)
        self.gameUI.bind("<Down>", self.__down_key_pressed_event)
        self.gameUI.bind("<Up>", self.__up_key_pressed_event)
