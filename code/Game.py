import Vehicle
from RushHourSearch import *
import time

EASY = "1"
NUM_OF_EASY_BOARDS = 20
MEDIUM = "2"
NUM_OF_MEDIUM_BOARDS = 12
HARD = "3"
NUM_OF_HARD_BOARDS = 8
HEURISTICS = {"1": null_heuristic,
    "2": distance_heuristic,
    "3": blocking_heuristic,
    "4": blocked_blocking_heuristic,
    "5": blocking_and_distance_heuristic,
    "6": blocked_and_distance_heuristic,
    "7": power_distance_heuristic,
    "8": manhattan_heuristic,
    "9": board_division_heuristic}
ALGORITHM = {"1": astar, "2": ida}


def parse_file(rushhour_file):
    """
    this function parses the rush hour game
    :param rushhour_file:
    :return:
    """
    file = open(rushhour_file)
    vehicles_list = []
    for line in file:
        if line.endswith('\n'):
            line = line[:-1]
        vehicle_id, x_coordinate, y_coordinate, direction = line
        vehicles_list.append(Vehicle(vehicle_id, int(x_coordinate), int(y_coordinate), direction))
    file.close()
    return vehicles_list


def get_game_file(difficulty):
    """
    select a board according to a given difficulty
    """
    if difficulty == EASY:
        random_game_number = np.random.randint(1, NUM_OF_EASY_BOARDS)
        return "easy" + str(random_game_number)  # should there be an extension like .txt
    if difficulty == MEDIUM:
        random_game_number = np.random.randint(1, NUM_OF_MEDIUM_BOARDS)
        return "medium" + str(random_game_number)  # should there be an extension like .txt
    if difficulty == HARD:
        random_game_number = np.random.randint(1, NUM_OF_HARD_BOARDS)
        return "hard" + str(random_game_number)  # should there be an extension like .txt


def get_move_direction(move, vehicles_list):
    """
    return a vehicle's move.
    """
    id = move.vehicle_id
    wanted_move = move.wanted_move
    for vehicle in vehicles_list:
        if vehicle.get_id() == id:
            if vehicle.get_direction() == 'H':
                if wanted_move == 1:
                    return "Right"
                else:
                    return "Left"
            else:
                if wanted_move == 1:
                    return "Down"
                else:
                    return "Up"


def print_backtrace(backtrace, vehicles_list, expanded):
    """
    this function prints the steps towards a solution.
    """
    last_board = None
    last_move = None
    print("Initial Board Game:")
    for current_board, move in backtrace:
        last_board = current_board
        last_move = move
        current_board.print_board()
        print()
        print("Move Vehicle " + move.vehicle_id + " " + get_move_direction(move, vehicles_list) + ": ")
    last_board.do_move(last_move).print_board()
    print("\nCongratulations! The game was solved in "+str(len(backtrace))+" steps, expanding "+ str(expanded)+ " nodes.")


def calculate_results_to_csv(level, index):
    """
    this function creates a csv file with the results of a run.
    """
    file = open('results.csv', 'w')
    file.write("Problem,Expanded nodes,Time,Solution length\n")
    file_name = level + str(index+1)
    path = "cards/" + file_name
    file.write(file_name + ",")
    vehicles_list = parse_file(path)
    rushHour = RushHourSearch(vehicles_list)
    print(file_name + "Level to solve:")
    rushHour.board.print_board()
    start = time.time()
    backtrace = ida_star(rushHour, blocking_heuristic)
    file.write(str(rushHour.expanded) + ",")
    end = time.time()
    file.write(str(end-start) + ",")
    file.write(str(len(backtrace)) + "\n")
    print_backtrace(backtrace, vehicles_list)


def solve_game_and_print(fileName, algorithm, heuristic):
    """

    :param fileName:
    :param algorithm:
    :param heuristic:
    :return:
    """
    path = "cards/" + fileName
    vehicles_list = parse_file(path)
    rushHour = RushHourSearch(vehicles_list)
    backtrace = algorithm(rushHour, heuristic)
    print_backtrace(backtrace, vehicles_list, rushHour.expanded)


if __name__ == '__main__':
    difficulty = input("Please choose difficulty of game:\n\tfor easy press 1\n\tfor medium press 2\n\tfor hard press 3\n")
    algorithm = input("Please choose a search algorithm to use:\n\t for A* press 1\n\t for IDA* press 2\n")
    heuristic = input("Please choose a heuristic for the search algorithm:"
                      "\n\t for null heuristic press 1"
                      "\n\t for distance heuristic press 2"
                      "\n\t for blocking cars heuristic press 3"
                      "\n\t for blocked blocking cars heuristic press 4"
                      "\n\t for blocking cars and distance heuristic press 5"
                      "\n\t for blocked blocking cars and distance heuristic press 6"
                      "\n\t for power of distance heuristic press 7"
                      "\n\t for manhattan distance heuristic press 8"
                      "\n\t for board division heuristic press 9\n")
    file_name = get_game_file(difficulty)
    print("Solving card "+file_name+"...")
    solve_game_and_print(file_name, ALGORITHM[algorithm], HEURISTICS[heuristic])
    print()
