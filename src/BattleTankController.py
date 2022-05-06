import sys
sys.path.append('../aima-python-master')

import time
import numpy as np

from search import simulated_annealing_full, exp_schedule
from threading import *
#import _thread

class BattleTankController():

    def __init__(self, model, view):
        self.__model = model
        self.__view = view
        self.__do_bindings()

    def show(self):
        self.__view.deiconify()

    def hide(self):
        self.__view.withdraw()

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
        self.__view.bind("<Left>", self.__left_key_pressed_event)
        self.__view.bind("<Right>", self.__right_key_pressed_event)
        self.__view.bind("<Down>", self.__down_key_pressed_event)
        self.__view.bind("<Up>", self.__up_key_pressed_event)

    def __do_update_enemy_position(self, enemy, action):
        current_enemy_position = self.__model.enemies_position[enemy]
        new_enemy_position = self.__model.update_enemy_position(enemy, action)

        if new_enemy_position is not None:
            # We need to update the UI
            row_index, col_index = current_enemy_position
            game_grid = self.get_game_grid()
            self.__view.update_image_cell(game_grid, row_index, col_index)
            row_index, col_index = new_enemy_position
            self.__view.update_image_cell(game_grid, row_index, col_index, action)

    def restart(self):
        self.__model.resetGrid()
        self.__view.dashboard.update_moves_count("-", "-")

    def get_game_grid(self):
        return self.__model.game_grid[:]

    def play_simulated_annealing(self):

        func = exp_schedule(k=20, lam=0.005, limit=100)

        # Get the solution and skip the first element (which is the initial state)
        self.__solution = simulated_annealing_full(self.__model, func)[1:]
        print(self.__solution)

    def confirm_play(self):
        
        t1=Thread(target=self.__run_simulation)
        t1.start()

    def __run_simulation(self):

        # Get the current player position
        current_player_position = self.__model.players_position["PLAYER_1"]

        # Here we do perform the updates in the UI according to the results of the algoritm
        index = 1
        total = len(self.__solution)

        for next_player_position in self.__solution:

            # Get the corresponding action for the state change
            action = self.__model.update_player_position("PLAYER_1", next_player_position)

            # Get a reference of the grid board
            game_grid = self.get_game_grid()

            # Get the indexes for both row and column of the current position and do update the UI 
            row_index, col_index = current_player_position
            self.__view.update_image_cell(game_grid, row_index, col_index)

            # Get the indexes for both row and column of the next position and do update the UI 
            row_index, col_index = next_player_position
            self.__view.update_image_cell(game_grid, row_index, col_index, action)

            current_player_position = tuple(next_player_position)

            # Do update the dashboard in the UI
            self.__view.dashboard.update_moves_count(index, total)
            index = index + 1

            time.sleep(0.5)
        