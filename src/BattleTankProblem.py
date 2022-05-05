import sys
sys.path.append('../aima-python-master')

from search import simulated_annealing_full, exp_schedule, Problem
import numpy as np

class BattleTank(Problem):
    def __init__(self, initial, game_grid = None, game_actions = None, game_representation = None):
        super().__init__(initial)

        # Actions
        self.__LEFT = 'LEFT'
        self.__UP = 'UP'
        self.__RIGHT = 'RIGHT'
        self.__DOWN = 'DOWN'

        # Characters in board
        self.__QUEEN = 'QUEEN'
        self.__PLAYER = 'PLAYER'
        self.__ENEMY = 'ENEMY'
        self.__WALL = 'WALL'
        self.__BRICK = 'BRICK'
        self.__ROAD = 'ROAD'

        self.game_actions = game_actions
        if self.game_actions is None:
            self.game_actions = {}
            self.game_actions[self.__LEFT] = (0, -1)
            self.game_actions[self.__UP] = (-1, 0)
            self.game_actions[self.__RIGHT] = (0, 1)
            self.game_actions[self.__DOWN] = (1, 0)

        self.game_representation = game_representation
        if self.game_representation is None:
            
            self.game_representation = {}
            self.game_representation[self.__QUEEN] = 0
            self.game_representation[self.__PLAYER] = 1
            self.game_representation[self.__ENEMY] = 2
            self.game_representation[self.__WALL] = 3
            self.game_representation[self.__BRICK] = 4
            self.game_representation[self.__ROAD] = 5
            
            self.game_representation_description = {}
            self.game_representation_description[self.game_representation[self.__QUEEN]] = self.__QUEEN
            self.game_representation_description[self.game_representation[self.__PLAYER]] = self.__PLAYER
            self.game_representation_description[self.game_representation[self.__ENEMY]] = self.__ENEMY
            self.game_representation_description[self.game_representation[self.__WALL]] = self.__WALL
            self.game_representation_description[self.game_representation[self.__BRICK]] = self.__BRICK
            self.game_representation_description[self.game_representation[self.__ROAD]] = self.__ROAD

        self.game_action_states = {}
        self.game_action_states[self.__LEFT] = [self.game_representation[self.__ENEMY], self.game_representation[self.__ROAD]]
        self.game_action_states[self.__UP] = [self.game_representation[self.__ENEMY], self.game_representation[self.__ROAD]]
        self.game_action_states[self.__RIGHT] = [self.game_representation[self.__ENEMY], self.game_representation[self.__ROAD]]
        self.game_action_states[self.__DOWN] = [self.game_representation[self.__ENEMY], self.game_representation[self.__ROAD]]

        self.queen_position = (9,5)
        self.initial_player_position = (9,1)
        self.initial_enemy_position = (1,9)

        self.enemies_position = {
            'ENEMY_1': self.initial_enemy_position
        }

        self.players_position = {
            'PLAYER_1': self.initial_player_position
        }

        # Grid initialization
        self.game_grid = game_grid
        if self.game_grid is None:
            self.rows_number = 11
            self.columns_number = 11
            self.resetGrid()
        
        self.rows_number = len(self.game_grid)
        assert self.rows_number > 0
        self.columns_number = len(self.game_grid[0])
        assert self.columns_number > 0
    
    def actions(self, state):
        # state is defined as the position in the grid where the player is currently positioned
        # state is implemented as a np-array of shape (1,2)

        # If there are no enemies, then game over
        if not np.any(self.game_grid == self.game_representation[self.__ENEMY]) or self.game_grid[tuple(state)] == self.game_grid[tuple(self.enemies_position['ENEMY_1'])]:
            return []
        
        # Otherwise, we explore the possible actions
        for possible_action in self.game_actions:
            if self.__isValidMove(state, possible_action):
                yield possible_action

    def result(self, state, action):
        # state is defined as the position in the grid where the player is currently positioned
        # state is implemented as a np-array of shape (1,2)
        # action is any of the keys for the game_actions dictionary
        # Here, we just need to validate if the action is any related with bullets
        # Which might could change the game grid other than just the basic move
        new_state = state + np.asarray(self.game_actions[action])
        return new_state
            
    def value(self, state):
        # state is defined as the position in the grid where the player is currently positioned
        # state is implemented as a np-array of shape (1,2)
        # Here, we want to evaluate how good is our current state
        # The value will be based on how far as an state I'm from the enemy
        # But also keeping into account how far is the enemy from the queen
        """
        queen_brick_count = np.count_nonzero(self.game_grid == self.game_representation['QUEEN'])
        is_enemy_alive = np.any(self.game_grid == self.game_representation['ENEMY'])
        """

        # distance between two points
        # Get the enemy position (for all the enemies)
        player_enemy_distances = {}
        queen_enemy_distances = {}
        for enemy in self.enemies_position:
            
            if  not np.array_equal(state - np.asarray(self.enemies_position[enemy]), np.asarray([0,0])):
                player_enemy_distances[enemy] = np.sqrt((state[0] - self.enemies_position[enemy][0])**2 + (state[1] - self.enemies_position[enemy][1])**2)
            #else:
            #    self.game_grid[tuple(state)] = self.game_representation[self.__PLAYER]

            if  not np.array_equal(np.asarray(self.queen_position) - np.asarray(self.enemies_position[enemy]), np.asarray([0,0])):
                queen_enemy_distances[enemy] = np.sqrt((self.queen_position[0] - self.enemies_position[enemy][0])**2 + (self.queen_position[1] - self.enemies_position[enemy][1])**2)
        
        if len(player_enemy_distances) == 0:
            return sys.maxsize
        elif len(queen_enemy_distances) == 0:
            return -1 * sys.maxsize

        # For now, we are going to assume there is only one enemy
        return 1 / player_enemy_distances[list(player_enemy_distances.keys())[0]] + queen_enemy_distances[list(queen_enemy_distances.keys())[0]] 
        #return self.game_grid[state]

    # PRIVATE METHODS

    def __isValidMove(self, state, action):

        # No move action is always a valid choice action
        if action == 'NO-MOVE':
            return True

        new_possible_state = state + np.asarray(self.game_actions[action])
        
        # Independently of the action (excepting NO-MOVE), will require to check the bounds
        if not (0 <= new_possible_state[0] <= self.rows_number - 1 and 0 <= new_possible_state[1] <= self.columns_number - 1):
            return False

        # When bounds are checked, then we just need to check also that the new state is consistent with the action
        return np.any(self.game_action_states[action] == self.game_grid[tuple(new_possible_state)])
        #return self.game_grid[new_possible_state] in self.game_action_states[action]
    
    def __setPositions(self):

        self.game_grid[self.initial_enemy_position] = self.game_representation[self.__ENEMY]
        self.game_grid[self.initial_player_position] = self.game_representation[self.__PLAYER]
        self.game_grid[self.queen_position] = self.game_representation[self.__QUEEN]
        
        self.game_grid[9,4] = self.game_representation[self.__BRICK]
        self.game_grid[9,6] = self.game_representation[self.__BRICK]
        self.game_grid[8,4] = self.game_representation[self.__BRICK]
        self.game_grid[8,5] = self.game_representation[self.__BRICK]
        self.game_grid[8,6] = self.game_representation[self.__BRICK]

    def __get_action(self, new_state, previous_state):
        
        move = tuple(new_state - previous_state)
        for action in self.game_actions:
            if self.game_actions[action] == move:
                return action
        return None

    # END PRIVATE METHODS

    # PUBLIC METHODS (NON PROBLEM CLASS)

    def resetGrid(self):
        self.game_grid = np.asarray(
            [
                [self.game_representation[self.__WALL]] * self.columns_number,
                [self.game_representation[self.__WALL]] + [self.game_representation[self.__ROAD]] * (self.columns_number - 2) + [self.game_representation[self.__WALL]],
                [self.game_representation[self.__WALL]] + [self.game_representation[self.__ROAD]] * (self.columns_number - 2) + [self.game_representation[self.__WALL]],
                [self.game_representation[self.__WALL]] + [self.game_representation[self.__ROAD]] * (self.columns_number - 2) + [self.game_representation[self.__WALL]],
                [self.game_representation[self.__WALL]] + [self.game_representation[self.__ROAD]] * (self.columns_number - 2) + [self.game_representation[self.__WALL]],
                [self.game_representation[self.__WALL]] + [self.game_representation[self.__ROAD]] * (self.columns_number - 2) + [self.game_representation[self.__WALL]],
                [self.game_representation[self.__WALL]] + [self.game_representation[self.__ROAD]] * (self.columns_number - 2) + [self.game_representation[self.__WALL]],
                [self.game_representation[self.__WALL]] + [self.game_representation[self.__ROAD]] * (self.columns_number - 2) + [self.game_representation[self.__WALL]],
                [self.game_representation[self.__WALL]] + [self.game_representation[self.__ROAD]] * (self.columns_number - 2) + [self.game_representation[self.__WALL]],
                [self.game_representation[self.__WALL]] + [self.game_representation[self.__ROAD]] * (self.columns_number - 2) + [self.game_representation[self.__WALL]],
                [self.game_representation[self.__WALL]] * self.columns_number,
            ]
        )

        self.enemies_position['ENEMY_1'] = self.initial_enemy_position
        self.players_position['PLAYER_1'] = self.initial_player_position

        self.__setPositions()

    def update_enemy_position(self, enemy, action):
        enemy_state = np.asarray(self.enemies_position[enemy])
        if self.__isValidMove(enemy_state, action):
            # Perform update in the game grid
            self.game_grid[tuple(enemy_state)] = self.game_representation[self.__ROAD]
            enemy_state = tuple(enemy_state + np.asarray(self.game_actions[action]))
            self.game_grid[enemy_state] = self.game_representation[self.__ENEMY]
            # do update the enemy position in the dict of enemies
            self.enemies_position[enemy] = enemy_state
            return enemy_state
            
        return None
    def viewStatesPath(self, statesPath):
        for i in range(len(statesPath)):
            if i < len(statesPath) -1:
                print("{} -> {}".format(statesPath[i], statesPath[i + 1]))

    def experiments(self, amount, k, lam, limit):
        func = exp_schedule(k, lam, limit)
        results = {}
        for i in range(amount):
            solution = simulated_annealing_full(self, func)
            self.resetGrid()
            keyResult = str(len(solution))
            if keyResult in results.keys():
                results[keyResult] += 1
            else:
                results[keyResult] = 1
        sortedKeys = list(results.keys())
        sortedKeys.sort(key=lambda x: int(x))

        return (results, sortedKeys)

    def update_player_position(self, player, next_player_state):
        
        current_player_state = np.asarray(self.players_position[player])
        action = self.__get_action(next_player_state, current_player_state)
        if action is None:
            raise "NoActionFoundError"

        elif not self.__isValidMove(current_player_state, action):
            print(self.game_grid)
            print("{} -> {} with {}".format(current_player_state, next_player_state, action))
            raise "InvalidMoveError"

        # Perform update in the game grid of the previous position
        self.game_grid[self.players_position[player]] = self.game_representation[self.__ROAD]
        # do update the player position in the dict of players
        self.players_position[player] = tuple(next_player_state)
        # Perform update in the game grid of the new position
        self.game_grid[self.players_position[player]] = self.game_representation[self.__PLAYER]

        return action

    # END PUBLIC METHODS (NON PROBLEM CLASS)

    