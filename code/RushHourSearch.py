from Board import *
import util

BFS = "BFS"
DFS = "DFS"

"""
RushHourSearch is the class representing the search problem
"""


class RushHourSearch:
    def __init__(self, vehicle_list):
        """
        Initialize the search problem with a board with a given vehicle list
        """
        self.board = Board(vehicle_list)
        self.expanded = 0

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        return self.board

    def is_goal_state(self, board):
        """
        board: Search state
        Returns True if and only if the state is a valid goal state
        """
        for i in range(2, 6):
            if i > board.player.x+1 and board.current_board[2][i] != ' ':
                return False
        return True

    def get_successors(self, board):
        """
        board: Search state
        For a given board, this should return a list of triples,
        (successor, move, stepCost), where 'successor' is a
        successor to the current state, 'move' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        self.expanded = self.expanded + 1
        return [(board.do_move(move), move, 1) for move in board.get_legal_moves()]


##########################
##########utils###########
##########################
def get_path(moves_dict, solution_board):
    """
    generate an array of all the boards and moves (as tuples)
    :param moves_dict: a dictionary with board keys and tuples of prev_board,
    move and cost as values.
    :param solution_board: the solved board
    :return: the array
    """
    action_array = []
    current_node = solution_board
    while current_node:
        tmp = moves_dict[current_node]
        current_node = tmp[0]
        if tmp[1] is not None:
            action_array.append((tmp[0], tmp[1]))
    action_array.reverse()
    return action_array


def current_board_is_visited(current_board, visited):
    """
    check if the current board was visited in the search
    :param current_board:
    :param visited: set of visited boards
    :return: true if and only if the board appears in visited boards set
    """
    for board in visited:
        if current_board.equals(board):
            return True


def vehicle_is_blocked(board, x_index):
    """
    this function checks if a car is blocked on the vertical axis.
    :param board:
    :param x_index:
    :return:
    """
    vehicle_id = board.current_board[2][x_index]
    cur_vehicle = get_vehicle(board, vehicle_id)
    y_bound = cur_vehicle.get_y_coordinate()
    vehicle_size = cur_vehicle.get_size()
    lower_bound = y_bound + vehicle_size - 1
    if ((y_bound == 0 or (y_bound > 0 and board.current_board[y_bound-1]
    [x_index] != ' '))
            and (lower_bound == 5 or (lower_bound < 5 and board.current_board
            [lower_bound+1][x_index] != ' '))):
        return True


def get_vehicle(board, index):
    """
    :param board:
    :param index:
    :return: return a Vehicle object for a given
    """
    for vehicle in board.vehicles_list:
        if vehicle.get_id() == index:
            return vehicle


class PQItem:
    def __init__(self, data):
        self.data = data


###############################
##########heuristics###########
###############################
def null_heuristic(board, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def distance_heuristic(board, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem. This is the distance from the goal state
    """
    x_index = board.get_player().get_x_coordinate()
    if x_index > 3:
        return 0
    return 4 - x_index


def power_distance_heuristic(board, problem=None):
    """
    A heuristic function estimates the cost from the current state to the
    nearest goal in the provided SearchProblem
    This is the distance from the goal state raised by the power of 10.
    """
    return distance_heuristic(board)**10


def blocking_heuristic(board, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  The blocking heuristic which is equal to zero at any goal state, and is equal
    to one plus the number of cars blocking the path to the exit in all other states.
    """
    counter = 0
    for i in range(2, 6):
        if i > board.player.x + 1 and board.current_board[2][i] != ' ':
            counter += 1
    return counter


def blocked_blocking_heuristic(board, problem=None):
    """
    A heuristic function estimates the cost from the current state to the
    nearest goal in the provided SearchProblem. the blocked blocking heuristic
    is like blocking heuristic where blocking car which is blocked too gain
    two points.
    """
    counter = 0
    for i in range(2, 6):
        if i > board.player.x + 1 and board.current_board[2][i] != ' ':
            if vehicle_is_blocked(board, i):
                counter += 1
            counter += 1
    return counter


def blocking_and_distance_heuristic(board, problem=None):
    """
    A heuristic function estimates the cost from the current state to the
    nearest goal in the provided SearchProblem. blocking and distance heuristic
    sums up the blocking heuristic and the distance heuristic.
    """
    return blocking_heuristic(board) + distance_heuristic(board)


def blocked_and_distance_heuristic(board, problem=None):
    """
    A heuristic function estimates the cost from the current state to the
    nearest goal in the provided SearchProblem. blocked and distance heuristic
    sums up the blocked heuristic and the distance heuristic.
    """
    return blocked_blocking_heuristic(board) + distance_heuristic(board)


def weight_heuristic(board, weight_function):
    """
    A general function which takes as an input a board and a weight function
    and returns the weighted value for all the occupied cell (which are not
    the player cell).
    """
    counter = 0
    x = board.player.get_x_coordinate()
    y = board.player.get_y_coordinate()
    board = board.current_board
    for i, row in enumerate(board):
        for j, col in enumerate(row):
            if board[i][j] != ' ' and board[i][j] != 'X':
                counter += weight_function(x, y, j, i)
    return counter


def calculate_manhattan_distance_helper(x_1, y_1, x_2, y_2):
    """
    this function returns 1 over the manhattan distance.
    """
    return 1 / (abs(x_1 - x_2) + abs(y_1 - y_2))


def manhattan_heuristic(board, problem=None):
    """
    A heuristic function estimates the cost from the current state to the
    nearest goal in the provided SearchProblem. the manhattan heuristic sums
    up 1 over the manhattan distances of the none occupied cells which are not
    the "X" car's position.
    """
    return weight_heuristic(board, calculate_manhattan_distance_helper)


def board_division_helper(x_1, y_1, x_2, y_2):
    """
    this function takes as an input two points p1 and p2 and returns the
    manhattan distance if x1 is on the left hand side of x2 and manhattan
    distance over 100 otherwise.
    """
    weight = calculate_manhattan_distance_helper(x_1, y_1, x_2, y_2)
    is_right = x_2 > x_1
    if is_right:
        return weight
    else:
        return weight / 100


def board_division_heuristic(board, problem=None):
    """
    A heuristic function estimates the cost from the current state to the
    nearest goal in the provided SearchProblem. this heuristic distinguish
    between points on the left hand side of the "X" car (red) and points on
    the right hand side.
    """
    return weight_heuristic(board, board_division_helper)


######################################
##########search algorithms###########
######################################
def general_search(problem, type):
    if type == DFS:
        fringe = util.Stack()
    elif type == BFS:
        fringe = util.Queue()
    else:
        return
    moves_dict = {}
    visited = set()
    # fringe is the data structure with a board and the cost of the move.
    fringe.push((problem.get_start_state(), None, 1))
    # moves dictionary is a dictionary for each board to its father and the cost of the action
    moves_dict[problem.get_start_state()] = (None, None, 1)
    while not fringe.isEmpty():
        current_board, current_move, current_cost = fringe.pop()
        if problem.is_goal_state(current_board):
            return get_path(moves_dict, current_board)
        if not current_board_is_visited(current_board, visited):
            visited.add(current_board)
            current_board_successors = problem.get_successors(current_board)
            for next_board, next_move, next_cost in current_board_successors:
                if not current_board_is_visited(next_board, visited) and \
                        next_board not in moves_dict.keys():
                    moves_dict[next_board] = (current_board, next_move, next_cost)
                    fringe.push((next_board, next_move, next_cost))
    return []


def depth_first_search(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches
    the goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.get_start_state().state)
    print("Is the start a goal?", problem.is_goal_state(problem.get_start_state()))
    print("Start's successors:", problem.get_successors(problem.get_start_state()))
    """
    return general_search(problem, DFS)


def breadth_first_search(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    return general_search(problem, BFS)


def a_star_search(problem, heuristic=null_heuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """
    fringe = util.PriorityQueue()
    moves_dict = {}
    visited = set()
    # fringe is the data structure with a board and the cost of the move.
    item = PQItem((problem.get_start_state(), None, 0))
    fringe.push(item, 0)
    # moves dictionary is a dictionary for each board to its father and the cost of the action
    moves_dict[problem.get_start_state()] = (None, None, 0)
    while not fringe.isEmpty():
        current_board, current_move, current_cost = fringe.pop().data
        if problem.is_goal_state(current_board):
            return get_path(moves_dict, current_board)
        if not current_board_is_visited(current_board, visited):
            visited.add(current_board)
            current_board_successors = problem.get_successors(current_board)
            for next_board, next_move, next_cost in current_board_successors:
                if not current_board_is_visited(next_board, visited) and \
                        next_board not in moves_dict.keys():
                    c = next_cost + moves_dict[current_board][2]
                    moves_dict[next_board] = (current_board, next_move, c)
                    item2 = PQItem((next_board, next_move, next_cost))
                    fringe.push(item2, c + heuristic(next_board, problem))
    return []


def ida_star(problem, heuristic=null_heuristic):
    """
    Iterative deepening A* heuristic. this function gets as an input a problem
    and an heuristic and solved the problem. this function use a heuristic
    function to evaluate the remaining cost to get to the goal from the A*
    search algorithm.
    """
    limit = heuristic(problem.get_start_state())
    counter = 0
    # todo: check counter
    while counter < 100000000:
        backtrace, limit, is_goal_state_flag = ida_star_helper(problem, heuristic, limit)
        if is_goal_state_flag:
            return backtrace
        counter += 1


def ida_star_helper(problem, heuristic=null_heuristic, limit=0):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """
    fringe = util.PriorityQueue()
    moves_dict = {}
    visited = set()
    # fringe is the data structure with a board and the cost of the move.
    item = PQItem((problem.get_start_state(), None, 0))
    fringe.push(item, 0)
    # moves dictionary is a dictionary for each board to its father and the cost of the action
    moves_dict[problem.get_start_state()] = (None, None, 0)
    new_limit = float('inf')
    while not fringe.isEmpty():
        current_board, current_move, current_cost = fringe.pop().data
        is_goal_state_flag = problem.is_goal_state(current_board)
        if is_goal_state_flag or current_cost > limit:
            return get_path(moves_dict, current_board), new_limit, is_goal_state_flag
        if not current_board_is_visited(current_board, visited):
            visited.add(current_board)
            current_board_successors = problem.get_successors(current_board)
            for next_board, next_move, next_cost in current_board_successors:
                if next_cost > limit and next_cost < new_limit:
                    new_limit = next_cost
                if not current_board_is_visited(next_board, visited) and next_board not in moves_dict.keys():
                    c = next_cost + moves_dict[current_board][2]
                    moves_dict[next_board] = (current_board, next_move, c)
                    item2 = PQItem((next_board, next_move, next_cost))
                    fringe.push(item2, c + heuristic(next_board, problem))
    return []


# Abbreviations
bfs = breadth_first_search
dfs = depth_first_search
astar = a_star_search
ida = ida_star
