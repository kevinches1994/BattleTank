import sys
sys.path.append('../aima-python-master')

from search import *

class BattleTank(Problem):
    def __init__(self, initial, game_grid = None, game_actions = None, game_representation = None):
        super().__init__(initial)

        self.game_actions = game_actions
        if self.game_actions is None:
            self.game_actions = {
                'LEFT': (0, -1),
                'UP': (-1, 0),
                'RIGHT': (0, 1),
                'DOWN': (1, 0)
                #,'SHOOT': (0, 0)
                #,'NO-MOVE': (0, 0)
                #'LEFT-WITH-BULLET': (0, -1), 
                #'UP-WITH-BULLET': (-1, 0), 
                #'RIGHT-WITH-BULLET': (0, 1), 
                #'DOWN-WITH-BULLET': (1, 0),
                
            }

        self.game_representation = game_representation
        if self.game_representation is None:
            
            self.game_representation_description = {
                0: 'QUEEN',
                1: 'PLAYER',
                2: 'ENEMY',
                3: 'WALL',
                4: 'BRICK',
                5: 'ROAD'
            }
            self.game_representation = {
                'QUEEN': 0,
                'PLAYER': 1,
                'ENEMY': 2,
                'WALL': 3,
                'BRICK': 4,
                'ROAD': 5
            }

        self.game_action_states = {
            'LEFT': [self.game_representation['ENEMY'], self.game_representation['ROAD']],
            'UP': [self.game_representation['ENEMY'], self.game_representation['ROAD']],
            'RIGHT': [self.game_representation['ENEMY'], self.game_representation['ROAD']],
            'DOWN': [self.game_representation['ENEMY'], self.game_representation['ROAD']]
            #,'LEFT-WITH-BULLET': [self.game_representation['ENEMY'], self.game_representation['BRICK'], self.game_representation['ROAD']], 
            #'UP-WITH-BULLET': [self.game_representation['ENEMY'], self.game_representation['BRICK'], self.game_representation['ROAD']],
            #'RIGHT-WITH-BULLET': [self.game_representation['ENEMY'], self.game_representation['BRICK'], self.game_representation['ROAD']],
            #'DOWN-WITH-BULLET': [self.game_representation['ENEMY'], self.game_representation['BRICK'], self.game_representation['ROAD']],
        }

        self.enemies_position = {
            'ENEMY_1': (1,9)
        }

        self.queen_position = (9,5)
        self.initial_player_position = (9,1)
        self.initial_enemy_position = (1,9)

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
        
        
    def resetGrid(self):
        self.game_grid = np.asarray(
            [
                [self.game_representation['WALL']] * self.columns_number,
                [self.game_representation['WALL']] + [self.game_representation['ROAD']] * (self.columns_number - 2) + [self.game_representation['WALL']],
                [self.game_representation['WALL']] + [self.game_representation['ROAD']] * (self.columns_number - 2) + [self.game_representation['WALL']],
                [self.game_representation['WALL']] + [self.game_representation['ROAD']] * (self.columns_number - 2) + [self.game_representation['WALL']],
                [self.game_representation['WALL']] + [self.game_representation['ROAD']] * (self.columns_number - 2) + [self.game_representation['WALL']],
                [self.game_representation['WALL']] + [self.game_representation['ROAD']] * (self.columns_number - 2) + [self.game_representation['WALL']],
                [self.game_representation['WALL']] + [self.game_representation['ROAD']] * (self.columns_number - 2) + [self.game_representation['WALL']],
                [self.game_representation['WALL']] + [self.game_representation['ROAD']] * (self.columns_number - 2) + [self.game_representation['WALL']],
                [self.game_representation['WALL']] + [self.game_representation['ROAD']] * (self.columns_number - 2) + [self.game_representation['WALL']],
                [self.game_representation['WALL']] + [self.game_representation['ROAD']] * (self.columns_number - 2) + [self.game_representation['WALL']],
                [self.game_representation['WALL']] * self.columns_number,
            ]
        )
        self.setPositions()

    def setPositions(self):

        self.game_grid[self.initial_enemy_position] = self.game_representation['ENEMY']
        self.game_grid[self.initial_player_position] = self.game_representation['PLAYER']
        self.game_grid[self.queen_position] = self.game_representation['QUEEN']
        
        self.game_grid[9,4] = self.game_representation['BRICK']
        self.game_grid[9,6] = self.game_representation['BRICK']
        self.game_grid[8,4] = self.game_representation['BRICK']
        self.game_grid[8,5] = self.game_representation['BRICK']
        self.game_grid[8,6] = self.game_representation['BRICK']

    def isValidMove(self, state, action):

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
    
    def actions(self, state):
        # state is defined as the position in the grid where the player is currently positioned
        # state is implemented as a np-array of shape (1,2)

        # If there are no enemies, then game over
        if not np.any(self.game_grid == self.game_representation['ENEMY']) or self.game_grid[tuple(state)] == self.game_grid[tuple(self.enemies_position['ENEMY_1'])]:
            return []
        
        # Otherwise, we explore the possible actions
        for possible_action in self.game_actions:
            if self.isValidMove(state, possible_action):
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
            else:
                self.game_grid[tuple(state)] = self.game_representation['PLAYER']

            if  not np.array_equal(np.asarray(self.queen_position) - np.asarray(self.enemies_position[enemy]), np.asarray([0,0])):
                queen_enemy_distances[enemy] = np.sqrt((self.queen_position[0] - self.enemies_position[enemy][0])**2 + (self.queen_position[1] - self.enemies_position[enemy][1])**2)
        
        if len(player_enemy_distances) == 0:
            return sys.maxsize
        elif len(queen_enemy_distances) == 0:
            return -1 * sys.maxsize

        # For now, we are going to assume there is only one enemy
        return 1 / player_enemy_distances[list(player_enemy_distances.keys())[0]] + queen_enemy_distances[list(queen_enemy_distances.keys())[0]] 
        #return self.game_grid[state]

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

    