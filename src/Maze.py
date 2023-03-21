import traceback
import sys
import Direction as Direction


# Class that holds all the maze data. This means the pheromones, the open and blocked tiles in the system as
# well as the starting and end coordinates.
class Maze:

    def __init__(self, walls, width, length):
        self.walls = walls
        self.length = length
        self.width = width
        self.start = None
        self.end = None
        self.initialize_pheromones()

    def get_distance_to_target(self, position, target):
        if abs(position.x - target.x) + abs(position.y - target.y) == 0:
            return 0.0000000000000000000001
        return abs(position.x - target.x) + abs(position.y - target.y)

    def is_accessible(self, position):
        x, y = position.x, position.y
        return self.in_bounds(position) and self.walls[x][y] != 0

    def initialize_pheromones(self):
        self.pheromones = [[1 if self.walls[x][y] == 1 else 0 for y in range(self.length)] for x in range(self.width)]

    def reset(self):
        self.initialize_pheromones()

    def add_pheromone_route(self, route, q):
        current_position = route.get_start()
        for direction in route.get_route():
            next_position = current_position.add_direction(direction)
            self.pheromones[current_position.x][current_position.y] += q / route.get_length()
            current_position = next_position

    def add_pheromone_routes(self, routes, q):
        for r in routes:
            self.add_pheromone_route(r, q)

    def evaporate(self, rho):
        for x in range(self.width):
            for y in range(self.length):
                if self.walls[x][y] == 1:
                    self.pheromones[x][y] *= (1 - rho)

    def get_width(self):
        return self.width

    def get_length(self):
        return self.length

    def get_surrounding_pheromone(self, position):
        pheromones = {}
        for direction in Direction.Direction:
            neighbor = position.add_direction(direction)
            if self.in_bounds(neighbor) and self.walls[neighbor.x][neighbor.y] == 1:
                pheromones[direction] = self.pheromones[neighbor.x][neighbor.y]
        return pheromones

    def get_pheromone(self, pos):
        if self.in_bounds(pos) and self.walls[pos.x][pos.y] == 1:
            return self.pheromones[pos.x][pos.y]
        return 0

    def in_bounds(self, position):
        return position.x_between(0, self.width) and position.y_between(0, self.length)

    def __str__(self):
        string = ""
        string += str(self.width)
        string += " "
        string += str(self.length)
        string += " \n"
        for y in range(self.length):
            for x in range(self.width):
                string += str(self.walls[x][y])
                string += " "
            string += "\n"
        return string

    # Method that builds a mze from a file
    # @param filePath Path to the file
    # @return A maze object with pheromones initialized to 0's inaccessible and 1's accessible.
    @staticmethod
    def create_maze(file_path):
        try:
            f = open(file_path, "r")
            lines = f.read().splitlines()
            dimensions = lines[0].split(" ")
            width = int(dimensions[0])
            length = int(dimensions[1])

            # make the maze_layout
            maze_layout = []
            for x in range(width):
                maze_layout.append([])

            for y in range(length):
                line = lines[y + 1].split(" ")
                for x in range(width):
                    if line[x] != "":
                        state = int(line[x])
                        maze_layout[x].append(state)
            print("Ready reading maze file " + file_path)
            return Maze(maze_layout, width, length)
        except FileNotFoundError:
            print("Error reading maze file " + file_path)
            traceback.print_exc()
            sys.exit()


