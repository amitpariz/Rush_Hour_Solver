import numpy as np
from Vehicle import *
from copy import deepcopy, copy


class Board:
    """
    A Board describes the current state of the game board.

    The Board stores:
    - board_w/board_h: the width and height of the playing area.
    - current_board: a 2D array of the board state.
    - player: the player vehicle, the one with id 'X'.
    - vehicles_list: A list of vehicles that exist in the board.
    """

    def __init__(self, vehicles_list):
        self.board_w = 6
        self.board_h = 6
        self.current_board = [[' ', ' ', ' ', ' ', ' ', ' '],
                              [' ', ' ', ' ', ' ', ' ', ' '],
                              [' ', ' ', ' ', ' ', ' ', ' '],
                              [' ', ' ', ' ', ' ', ' ', ' '],
                              [' ', ' ', ' ', ' ', ' ', ' '],
                              [' ', ' ', ' ', ' ', ' ', ' ']]
        self.vehicles_list = vehicles_list
        self.player = self.get_player()
        self.mark_board()

    def get_player(self):
        for vehicle in self.vehicles_list:
            if vehicle.get_id() == 'X':
                return vehicle

    def mark_board(self):
        """
        Updates the cuurent board according to all the vehicles positions.
        """
        updated_board = [[' ', ' ', ' ', ' ', ' ', ' '],
                         [' ', ' ', ' ', ' ', ' ', ' '],
                         [' ', ' ', ' ', ' ', ' ', ' '],
                         [' ', ' ', ' ', ' ', ' ', ' '],
                         [' ', ' ', ' ', ' ', ' ', ' '],
                         [' ', ' ', ' ', ' ', ' ', ' ']]
        for vehicle in self.vehicles_list:
            for i in range(vehicle.get_size()):
                if vehicle.get_direction() == 'H':
                    updated_board[vehicle.get_y_coordinate()][vehicle.get_x_coordinate()+i] = vehicle.get_id()
                else:
                    updated_board[vehicle.get_y_coordinate()+i][vehicle.get_x_coordinate()] = vehicle.get_id()
            self.current_board = updated_board

    def add_move(self, move):
        """
        Try to add the given move to the board.
        If the move is legal, the board state is updated; if it's not legal, a
        ValueError is raised.
        """
        if not self.check_move_valid(move):
            raise ValueError("Move is invalid")

        for vehicle in self.vehicles_list:
            if vehicle.get_id() == move.vehicle_id:
                if vehicle.get_direction() == 'H':
                    vehicle.set_x_coordinate(vehicle.get_x_coordinate() + move.wanted_move)
                    break
                else:
                    vehicle.set_y_coordinate(vehicle.get_y_coordinate() + move.wanted_move)
                    break

        self.mark_board()

    def do_move(self, move):
        """
        Performs a move, returning a new board
        """
        new_board = self.__copy__()
        new_board.add_move(move)

        return new_board

    def get_legal_moves(self):
        """
        Returns a list of legal moves for the current board state.
        """
        # Generate all legal moves
        moves_list = []
        for vehicle in self.vehicles_list:
            forward_move = Move(vehicle.get_id(), 1)
            if self.check_move_valid(forward_move):
                moves_list.append(forward_move)
            backward_move = Move(vehicle.get_id(), -1)
            if self.check_move_valid(backward_move):
                moves_list.append(backward_move)

        return moves_list

    def check_valid_id(self, move_id):
        """
        Check if the vehicle we want to move exist in the current board.
        """
        for vehicle in self.vehicles_list:
            if move_id == vehicle.get_id():
                return True
        return False

    def check_move_valid(self, move):
        """
        Check if given move is a legal move, meaning the wanted vehicle can move in the wanted direction.
        """
        if not self.check_valid_id(move.vehicle_id):
            return False

        for vehicle in self.vehicles_list:
            if vehicle.get_id() == move.vehicle_id:
                if vehicle.get_direction() == 'H':
                    if move.wanted_move == -1:
                        if vehicle.get_x_coordinate() - 1 < 0:
                            return False
                        return self.current_board[vehicle.get_y_coordinate()][vehicle.get_x_coordinate() - 1] == ' '
                    if vehicle.get_end_x_coordinate() + 1 > 5:
                        return False
                    return self.current_board[vehicle.get_y_coordinate()][vehicle.get_end_x_coordinate() + 1] == ' '
                else:
                    if move.wanted_move == -1:
                        if vehicle.get_y_coordinate() - 1 < 0:
                            return False
                        return self.current_board[vehicle.get_y_coordinate() - 1][vehicle.get_x_coordinate()] == ' '
                    if vehicle.get_end_y_coordinate() + 1 > 5:
                        return False
                    return self.current_board[vehicle.get_end_y_coordinate() + 1][vehicle.get_x_coordinate()] == ' '

    def check_tile_legal(self, x, y):
        """
        Check if the tile in the y'th row and x'th column is free.
        """
        return self.current_board[y][x] == ' '

    def get_position(self, x, y):
        """
        :return: the id of the car in the y'th row and x'th column, or space if there is no car there
        """
        return self.current_board[y][x]

    def print_board(self):
        board = deepcopy(self.current_board)
        for i, col in enumerate(board):
            cur_col = ""
            for j, row in enumerate(col):
                if board[i][j] == ' ':
                    board[i][j] = '_'
                cur_col += board[i][j]
            print(cur_col)

    def __copy__(self):
        cpy_board = Board(deepcopy(self.vehicles_list))
        cpy_board.board_w = 6
        cpy_board.board_h = 6
        cpy_board.current_board = np.copy(self.current_board)
        return cpy_board

    def equals(self, other):
        """
        Two board objects are equal if their current boards are the same (all
        vehicles are in the same places)
        """
        if self.current_board == other.current_board:
            return True
        return False


class Move:
    """
    Describes a move.
    It contains:
    - id: the ID of the vehicle being used
    - wanted_move: +1 if we want to move the car forward (down if vertical, right if horizontal),
     -1 if we want to move it backward (up if vertical, left if horizontal)
    """

    def __init__(self, id, wanted_move):
        self.vehicle_id = id
        self.wanted_move = wanted_move
