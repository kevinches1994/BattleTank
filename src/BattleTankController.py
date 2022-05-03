class BattleTankController():

    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.__do_bindings()

    def show(self):
        self.view.deiconify()

    def hide(self):
        self.view.withdraw()

    def __left_key_pressed_event(self, event):
        self.__do_update_enemy_position('ENEMY_1', 'LEFT')

    def __right_key_pressed_event(self, event):
        self.__do_update_enemy_position('ENEMY_1', 'RIGHT')

    def __up_key_pressed_event(self, event):
        self.__do_update_enemy_position('ENEMY_1', 'UP')

    def __down_key_pressed_event(self, event):
        self.__do_update_enemy_position('ENEMY_1', 'DOWN')

    def __do_bindings(self):
        #self.view.bind("<Key>", self.__key_pressed)
        #self.view.bind("<Key>", lambda event: print("Key {} was pressed".format(event)))
        self.view.bind("<Left>", self.__left_key_pressed_event)
        self.view.bind("<Right>", self.__right_key_pressed_event)
        self.view.bind("<Down>", self.__down_key_pressed_event)
        self.view.bind("<Up>", self.__up_key_pressed_event)

    def __do_update_enemy_position(self, enemy, action):
        current_enemy_position = self.model.enemies_position[enemy]
        new_enemy_position = self.model.update_enemy_position(enemy, action)

        if new_enemy_position is not None:
            # We need to update the UI
            row_index = current_enemy_position[0]
            col_index = current_enemy_position[1]
            self.view.put_image_label(self.view.game_ui_grid[row_index][col_index], self.model.game_grid, row_index, col_index)
            row_index = new_enemy_position[0]
            col_index = new_enemy_position[1]
            self.view.put_image_label(self.view.game_ui_grid[row_index][col_index], self.model.game_grid, row_index, col_index, action)

    def restart(self):
        self.model.resetGrid()

    def get_game_grid(self):
        return self.model.game_grid