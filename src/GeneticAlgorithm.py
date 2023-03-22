import random
import numpy as np
from TSPData import TSPData

class GeneticAlgorithm:

    def __init__(self, generations, pop_size, elite, mutation_rate):
        self.generations = generations
        self.pop_size = pop_size
        self.elite = elite
        self.mutation_rate = mutation_rate

        # This method should solve the TSP.
        # @param pd the TSP data.
        # @return the optimized product sequence.

    def solve_tsp(self, tsp_data):
        self.tsp_data = tsp_data
        self.city_count = 18

        # Generate initial population
        self.population = self._generate_initial_population()

        # Loop through generations
        for i in range(self.generations):
            self._next_generation()

        # Return the best route
        return self._get_best_route()

    # Generates the initial population randomly.
    def _generate_initial_population(self):
        population = []
        for i in range(self.pop_size):
            population.append(random.sample(range(self.city_count), self.city_count))
        return population


    # Calculates the Euclidean distance between two cities.
    def _distance(self, city_a, city_b):
        return np.linalg.norm(city_a - city_b)

        # Generates the next generation.

    def _next_generation(self):
        # Keep the top performing route from the previous generation
        elite_count = int(self.elite * self.pop_size)
        elites = self._get_elites(elite_count)

        # Generate new population
        new_population = elites
        for i in range(self.pop_size - elite_count):
            parent_a = self._select_parent()
            parent_b = self._select_parent()
            child, child2 = self._crossover(parent_a, parent_b)

            # Apply mutation to some children
            if random.random() < self.mutation_rate:
                child = self._mutate(child)
            if random.random() < self.mutation_rate:
                child2 = self._mutate(child2)

            new_population.append(child)
            new_population.append(child2)

        # Select the best route from the current population
        best_route, _ = self._get_best_route()
        new_population[0] = best_route

        # Update the population
        self.population = new_population

    # Selects the top performing routes from the population.
    def _get_elites(self, elite_count):
        routes = [(route, self._get_route_distance(route)) for route in self.population]
        routes.sort(key=lambda x: x[1])
        elites = [route[0] for route in routes[:elite_count]]
        return elites


    # Selects a parent for breeding.
    def _select_parent(self):
        return random.choice(self.population)

    def _mutate(self, child):
        for i in range(len(child)):
            if random.random() < self.mutation_rate:
                j = random.randint(0, len(child) - 1)
                child[i], child[j] = child[j], child[i]
        return child

    # Performs crossover between two parents.
    def _crossover(self, parent_a, parent_b):
        # Initialize empty child routes
        child = [-1] * self.city_count
        child2 = [-1] * self.city_count

        # Randomly select a segment of the first parent and copy it to the corresponding segment of one child
        start_pos = random.randint(0, self.city_count - 1)
        end_pos = random.randint(0, self.city_count - 1)

        if start_pos > end_pos:
            start_pos, end_pos = end_pos, start_pos

        for i in range(start_pos, end_pos + 1):
            child[i] = parent_a[i]
            child2[i] = parent_b[i]

        # Fill in the remaining cities from the second parent in the order in which they appear in the second parent,
        # skipping any cities that have already been included in the segment copied from the first parent
        for i in range(self.city_count):
            if parent_b[i] not in child:
                for j in range(self.city_count):
                    if child[j] == -1:
                        child[j] = parent_b[i]
                        break

        for i in range(self.city_count):
            if parent_a[i] not in child2:
                for j in range(self.city_count):
                    if child2[j] == -1:
                        child2[j] = parent_a[i]
                        break

        return child, child2
    def _get_best_route(self):
        best_route = None
        best_distance = float('inf')

        for route in self.population:
            distance = self._get_route_distance(route)

            if distance < best_distance:
                best_distance = distance
                best_route = route

        return best_route, best_distance

    def _get_route_distance(self, route):
        distances = self.tsp_data.distances
        distance = self.tsp_data.get_start_distances()[route[0]]
        for i in range(len(route) - 1):
            from_city = route[i]
            to_city = route[i + 1]
            distance += distances[from_city][to_city]
        distance += self.tsp_data.get_end_distances()[route[-1]]
        return distance
