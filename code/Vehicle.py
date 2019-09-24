
available_vehicles = {'X': 2, 'A': 2, 'B': 2, 'C': 2, 'D': 2, 'E': 2, 'F': 2, 'G': 2, 'H': 2, 'I': 2,
                      'J': 2, 'K': 2, 'O': 3, 'P': 3, 'Q': 3, 'R': 3}


class Vehicle:
    """
    Represents a vehicle object. the x and y coordinates refer to the left most coordinate if it is
    a horizontal vehicle and to the top most coordinate if it is a vertical vehicle.
    The direction is 'H' if the vehicle is horizontal and 'V' if it is vertical.
    All vehicles X,A,B,C,D,E,F,G,I,J,K are cars and their size is 2, while O,P,Q,R are trucks
    and their size is 3.
    """
    def __init__(self, id, x, y, direction):
        self.id = id
        self.x = y
        self.y = x
        self.direction = direction
        self.size = available_vehicles[id]

    def get_id(self):
        return self.id

    def get_x_coordinate(self):
        return self.x

    def get_y_coordinate(self):
        return self.y

    def get_end_x_coordinate(self):
        if self.direction == 'H':
            return self.x + self.size - 1
        else:
            return self.x

    def get_end_y_coordinate(self):
        if self.direction == 'H':
            return self.y
        else:
            return self.y + self.size - 1

    def get_direction(self):
        return self.direction

    def get_size(self):
        return self.size

    def set_x_coordinate(self, new_x):
        self.x = new_x

    def set_y_coordinate(self, new_y):
        self.y = new_y
