import numpy as np

from src.Ant import Ant


# Class representing the first assignment. Finds shortest path between two points in a maze according to a specific
# path specification.
class AntColonyOptimization:
# Class representing the first assignment. Finds shortest path between two points in a maze according to a specific
# path specification.
    def __init__(self, maze, ants_per_gen, generations, q, evaporation, alpha=1, beta=1):
        self.maze = maze
        self.ants_per_gen = ants_per_gen
        self.generations = generations
        self.q = q
        self.evaporation = evaporation
        self.alpha = alpha
        self.beta = beta


    def find_shortest_route(self, path_specification):
        self.maze.reset()
        shortest_route = None
        shortest_route_length = float('inf')

        for _ in range(self.generations):

            ant_routes = []
            ant_route_lengths = []

            for _ in range(self.ants_per_gen):
                ant = Ant(self.maze, path_specification, self.alpha, self.beta)
                route = ant.find_route()
                route_length = len(route.route)
                ant_routes.append(route)
                ant_route_lengths.append(len(route.route))

                if route_length < shortest_route_length:
                    shortest_route_length = route_length
                    shortest_route = route

            self.maze.add_pheromone_routes(ant_routes, self.q)
            self.maze.evaporate(self.evaporation)

        return shortest_route