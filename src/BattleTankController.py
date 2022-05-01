class BattleTankController():

    def __init__(self, problem, gameUI):
        self.problem = problem
        self.gameUI = gameUI

    def show(self):
        self.gameUI.deiconify()