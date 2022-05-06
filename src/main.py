from BattleTankProblem import *
from BattleTankUI import *
from BattleTankController import *

import sys

if __name__ == "__main__":

    #print('cmd entry:', sys.argv)
    assert len(sys.argv) == 4

    #sys.argv[1] must be "x,y"
    assert len(sys.argv[1]) > 0
    initial = np.asarray(list(eval(sys.argv[1])))

    # args 2 and 3 must be numbers
    rows = int(sys.argv[2])
    cols = int(sys.argv[3])

    # rows and cols greater than the initial state pair
    assert rows > initial[0]
    assert cols > initial[1]

    # board is a square matrix
    assert rows == cols

    problem = BattleTank(initial, rows, cols)
    gameUI = BattleTankUI(problem.rows_number, problem.columns_number, problem.game_grid)
    controller = BattleTankController(problem, gameUI)
    gameUI.set_controller(controller)
    gameUI.mainloop()