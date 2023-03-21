import random
from Route import Route

#Class that represents the ants functionality.
class Ant:
    def __init__(self, maze, path_specification, alpha, beta):
        self.maze = maze
        self.start = path_specification.get_start()
        self.end = path_specification.get_end()
        self.current_position = self.start
        self.alpha = alpha
        self.beta = beta

    def find_route(self):
        route = Route(self.start)
        visited = {self.start}

        while self.current_position != self.end:
            next_move = self.choose_next_move(visited)
            if next_move is None:
                # No available moves, backtrack
                last_move = route.remove_last()
                self.current_position = self.current_position.subtract_direction(last_move)
            else:
                direction, next_position = next_move
                route.add(direction)
                visited.add(next_position)
                self.current_position = next_position

        return route

    def choose_next_move(self, visited):
        pheromone_data = self.maze.get_surrounding_pheromone(self.current_position)
        available_moves = [
            (direction, self.current_position.add_direction(direction))
            for direction, pheromone in pheromone_data.items()
            if self.maze.in_bounds(self.current_position.add_direction(direction)) and self.current_position.add_direction(direction) not in visited and self.maze.is_accessible(self.current_position.add_direction(direction))
        ]

        if not available_moves:
            return None


        probabilities = [
            (pheromone_data[direction] ** self.alpha) * ((1 / self.maze.get_distance_to_target(position, self.end)) ** self.beta)
            for direction, position in available_moves
        ]

        total = sum(probabilities)
        probabilities = [p / total for p in probabilities]

        chosen_direction, chosen_position = random.choices(available_moves, probabilities)[0]
        return chosen_direction, chosen_position