from BattleTankProblem import *
from BattleTankUI import *
from BattleTankController import *

if __name__ == "__main__":
    initial = np.asarray([9,1])
    problem = BattleTank(initial)
    gameUI = BattleTankUI(problem.rows_number, problem.columns_number, problem.game_grid)
    controller = BattleTankController(problem, gameUI)
    gameUI.set_controller(controller)
    gameUI.mainloop()