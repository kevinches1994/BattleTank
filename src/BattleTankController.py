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
        self.__do_update_enemy_position('ENEMY_1', 'LEFT')

    def __right_key_pressed_event(self, event):
        self.__do_update_enemy_position('ENEMY_1', 'RIGHT')

    def __up_key_pressed_event(self, event):
        self.__do_update_enemy_position('ENEMY_1', 'UP')

    def __down_key_pressed_event(self, event):
        self.__do_update_enemy_position('ENEMY_1', 'DOWN')

    def __do_bindings(self):
        #self.gameUI.bind("<Key>", self.__key_pressed)
        #self.gameUI.bind("<Key>", lambda event: print("Key {} was pressed".format(event)))
        self.gameUI.bind("<Left>", self.__left_key_pressed_event)
        self.gameUI.bind("<Right>", self.__right_key_pressed_event)
        self.gameUI.bind("<Down>", self.__down_key_pressed_event)
        self.gameUI.bind("<Up>", self.__up_key_pressed_event)

    def __do_update_enemy_position(self, enemy, action):
        current_enemy_position = self.problem.enemies_position[enemy]
        new_enemy_position = self.problem.update_enemy_position(enemy, action)

        if new_enemy_position is not None:
            # We need to update the UI
            row_index = current_enemy_position[0]
            col_index = current_enemy_position[1]
            self.gameUI.put_image_label(self.gameUI.game_ui_grid[row_index][col_index], self.problem.game_grid, row_index, col_index)
            row_index = new_enemy_position[0]
            col_index = new_enemy_position[1]
            self.gameUI.put_image_label(self.gameUI.game_ui_grid[row_index][col_index], self.problem.game_grid, row_index, col_index, action)