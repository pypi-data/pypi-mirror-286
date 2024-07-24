#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author  : nickdecodes
@Email   : nickdecodes@163.com
@Usage   :
@FileName: genetics_util.py
@DateTime: 2024/7/22 10:23
@SoftWare: PyCharm
"""

import random
import numpy as np


class GeneticsUtil:
    def __init__(self, refers: list, data: list, min_num: int, max_num: int, fitness_params: dict,
                 population_size: int = 100, num_genes: int = 5, tournament_size: int = 3,
                 mutation_rate: float = 0.1, epoch_count: int = 100):
        """
        Initializes the GeneticsUtil class with the necessary parameters for the genetic algorithm.

        Args:
        refers (list): Reference matrix or data used for creating the reference matrix.
        data (list): Dataset from which genes are selected.
        min_num (int): Minimum allowable value for a gene.
        max_num (int): Maximum allowable value for a gene.
        fitness_params (dict): Parameters used for calculating fitness.
        population_size (int): Number of individuals in the population.
        num_genes (int): Number of genes in each individual.
        tournament_size (int): Size of the tournament for selection process.
        mutation_rate (float): Probability of mutation per gene.
        epoch_count (int): Number of generations or epochs the algorithm will run.
        """
        self.refers = refers
        self.data = data
        self.min_num = min_num
        self.max_num = max_num
        self.fitness_params = fitness_params
        self.population_size = population_size
        self.num_genes = num_genes
        self.tournament_size = tournament_size
        self.mutation_rate = mutation_rate
        self.epoch_count = epoch_count
        self.population = self.init_population()  # Initializes the population
        self.refers_matrix = self.create_refers_matrix()  # Creates a matrix from reference data

    def init_population(self) -> list:
        """
        Initializes the population with randomly selected, non-repeating genes from the data set.

        Returns:
        list: A list of individuals, each represented as a sorted list of genes.
        """
        population = [np.random.choice(self.data, self.num_genes, replace=False) for _ in range(self.population_size)]
        sorted_population = [np.sort(row) for row in population]
        return sorted_population

    def create_refers_matrix(self) -> list:
        """
        Creates a matrix based on the reference data provided during initialization.

        Returns:
        list: A matrix where each row corresponds to an item in the reference data,
              with binary encoding based on the presence of elements within the specified range.
        """
        refers_matrix = []
        for row in self.refers:
            vector = [0] * self.max_num  # Initialize vector of length max_num with zeros
            for num in row:
                if self.min_num <= num <= self.max_num:
                    vector[num - 1] = 1  # Set the corresponding position to 1
            refers_matrix.append(vector)
        return refers_matrix

    def check_diagonal(self, individual: list, dfs_size: tuple = (3, 3)) -> float:
        """
        Checks diagonal alignments in a dynamically updated matrix based on the individual's genes
        and evaluates their fitness based on the alignment.

        Args:
        individual (list): List of gene indices representing an individual in the population.
        dfs_size (tuple): Size of the matrix region to check for diagonal alignments (rows, cols).

        Returns:
        float: A fitness value modified based on the presence of diagonal alignments.
        """
        fitness_value = 1
        pre_index = individual[0] - 1  # Previous index for diagonal checking

        for indi in individual:
            if not (self.min_num <= indi <= self.max_num):
                return 1  # Return a default fitness value if gene is out of valid range

            num_index = indi - 1
            rows = len(self.refers_matrix)
            cols = self.max_num
            dfs_row, dfs_col = dfs_size
            is_balance = dfs_row == dfs_col  # Check if the area to be checked is a square
            target = min(dfs_size)

            if dfs_row > rows or dfs_col > cols:
                continue  # Skip if the matrix is smaller than the dfs size

            # Create a new matrix including a new row for the current gene
            new_matrix = [row[:] for row in self.refers_matrix]  # Copy the existing matrix
            new_row = [0] * self.max_num
            new_row[num_index] = 1
            new_matrix.append(new_row)  # Add the new row correctly

            # Check diagonals, only upwards
            for dr in [-1]:  # Only need to check the upper diagonals
                move_r = False
                move_r_count = 0
                move_c_count = 0
                for dc in [-1, 1]:  # Check both left and right diagonals
                    count = 0
                    r, c = rows, num_index
                    while rows - dfs_row <= r <= rows + 1 and pre_index - dfs_col <= c <= num_index + dfs_col:
                        if new_matrix[r][c] == 1:
                            count += 1
                        if is_balance:
                            r += dr
                            c += dc
                        else:
                            if move_r:
                                if new_matrix[r][c] == 1:
                                    move_c_count += 1
                                r += dr
                                move_r = False
                            else:
                                if new_matrix[r][c] == 1:
                                    move_r_count += 1
                                c += dc
                                move_r = True

                    if is_balance and count == target:
                        fitness_value *= 0.1  # Decrease fitness if a balanced diagonal is found
                    elif not is_balance and max(move_r_count, move_c_count) == target - 1:
                        fitness_value *= 0.3  # Decrease fitness if an unbalanced diagonal is found

            pre_index = num_index  # Update previous index for the next gene

        return fitness_value

    def check_vertical(self, individual: list) -> float:
        """
        Checks vertical alignments in a dynamically updated matrix based on the individual's genes
        and evaluates their fitness based on the alignment.

        Args:
        individual (list): List of gene indices representing an individual in the population.

        Returns:
        float: A fitness value modified based on the presence of vertical alignments.
        """
        fitness_value = 1
        pre_index = individual[0] - 1  # Previous index, unused in vertical checking

        for indi in individual:
            if not (self.min_num <= indi <= self.max_num):
                return 1  # Return a default fitness value if gene is out of valid range

            num_index = indi - 1
            rows = len(self.refers_matrix)

            # Create a new matrix including a new row for the current gene
            new_matrix = [row[:] for row in self.refers_matrix]  # Copy the existing matrix
            new_row = [0] * self.max_num
            new_row[num_index] = 1
            new_matrix.append(new_row)  # Add the new row correctly

            # Check vertical alignment
            for dr in [-1]:  # Only need to check the upward vertical line
                count = 0
                r, c = rows, num_index
                while 0 <= r < len(new_matrix):
                    if new_matrix[r][c] == 1:
                        count += 1
                    else:
                        # Check if there are no genes in the current column in the original matrix
                        if sum(new_matrix[row][c] for row in range(rows)) == 0:
                            fitness_value *= 0.5
                        elif count > 1:
                            fitness_value *= 0.4
                        else:
                            fitness_value = 1
                    r += dr

                # Adjust fitness based on the count of vertical alignments
                if count in range(1, 3):
                    fitness_value *= 0.1
                else:
                    fitness_value *= 0.7

            pre_index = num_index  # Update previous index for the next gene

        return fitness_value

    def fitness(self, individual: list, dfs_size: tuple = (2, 2)) -> float:
        """
        Calculates the fitness of an individual based on the alignment of genes in a dynamically
        updated matrix. Fitness is evaluated based on specific alignment patterns and parameters.

        Args:
        individual (list): List of gene indices representing an individual in the population.
        dfs_size (tuple): Size of the matrix region to check for alignments (rows, cols).

        Returns:
        float: A fitness value modified based on the presence of specific alignments.
        """
        # return np.linalg.norm(individual - target)
        # Check for duplicate genes, which are not allowed
        if len(set(individual)) < self.num_genes:
            return 10000  # High penalty for duplicate genes

        fitness_value = 1
        pre_index = individual[0] - 1  # Previous index for alignment checking

        for indi in individual:
            # Check if the gene is within the valid range
            if not (self.min_num <= indi <= self.max_num):
                return 10000  # High penalty for out-of-range genes

            num_index = indi - 1
            rows, cols = len(self.refers_matrix), self.max_num
            (dfs_row, dfs_col), target = dfs_size, min(dfs_size)

            # Check if the dfs_size is larger than the matrix dimensions
            if dfs_row > rows or dfs_col > cols:
                return 1  # Return default fitness if the dfs size is too large

            # Create a new matrix including a new row for the current gene
            new_matrix = [row[:] for row in self.refers_matrix]  # Copy the existing matrix
            new_row = [0] * self.max_num
            new_row[num_index] = 1
            new_matrix.append(new_row)  # Add the new row correctly

            # Check alignments only upwards
            for dr in [-1]:  # Only need to check the upward direction
                # Check diagonals
                move_r = False
                move_r_count = 0
                move_c_count = 0
                for dc in [-1, 1]:  # Check both left and right diagonals
                    count = 0
                    r, c = rows, num_index
                    while rows - dfs_row <= r <= rows + 1 and pre_index - dfs_col <= c <= min(num_index + dfs_col,
                                                                                              cols - 1):
                        if new_matrix[r][c] == 1:
                            count += 1
                        if dfs_row == dfs_col:
                            r += dr
                            c += dc
                        else:
                            if move_r:
                                if new_matrix[r][c] == 1:
                                    move_c_count += 1
                                r += dr
                                move_r = False
                            else:
                                if new_matrix[r][c] == 1:
                                    move_r_count += 1
                                c += dc
                                move_r = True

                    # Adjust fitness based on the count of diagonal alignments
                    if dfs_row == dfs_col and count == target:
                        fitness_value *= self.fitness_params[0]
                    elif not dfs_row == dfs_col and max(move_r_count, move_c_count) == target - 1:
                        fitness_value *= self.fitness_params[1]

                # Check vertical alignment
                count = 0
                r, c = rows, num_index
                while 0 <= r < len(new_matrix):
                    if new_matrix[r][c] == 1:
                        count += 1
                    else:
                        # Check if there are no genes in the current column in the original matrix
                        if sum(new_matrix[row][c] for row in range(rows)) == 0:
                            fitness_value *= self.fitness_params[2]
                        elif count > 1:
                            fitness_value *= self.fitness_params[3]
                        else:
                            fitness_value = self.fitness_params[4]
                    r += dr

                # Adjust fitness based on the count of vertical alignments
                if count in range(1, 3):
                    fitness_value *= self.fitness_params[5]
                else:
                    fitness_value *= self.fitness_params[6]

            pre_index = num_index  # Update previous index for the next gene

        return fitness_value

    def tournament_selection(self) -> np.ndarray:
        """
        Tournament selection method. Randomly selects k individuals from the population
        and returns the individual with the highest fitness.

        Returns:
        np.ndarray: The individual with the highest fitness from the selected sample.
        """
        # Select the individual with the highest fitness from a random sample
        selected = max(random.sample(self.population, self.tournament_size), key=lambda ind: 1 / self.fitness(ind))
        # Sort the selected individual for consistency
        sorted_selected = np.sort(selected)
        return sorted_selected

    def crossover(self, parent1: np.ndarray, parent2: np.ndarray) -> np.ndarray:
        """
        Two-point crossover. Randomly selects two points and swaps the genes between the two parents
        to create a child.

        Args:
        parent1 (np.ndarray): The first parent.
        parent2 (np.ndarray): The second parent.

        Returns:
        np.ndarray: The child created by crossover.
        """
        # Randomly select two points for crossover
        points = sorted(random.sample(range(0, self.num_genes), 2))
        # Create new child by combining parts of both parents
        return np.concatenate([parent1[:points[0]], parent2[points[0]:points[1]], parent1[points[1]:]])

    def mutate(self, individual: np.ndarray) -> np.ndarray:
        """
        Mutation operation. Mutates an individual's gene with a certain probability.

        Args:
        individual (np.ndarray): The individual to mutate.

        Returns:
        np.ndarray: The mutated individual.
        """
        # Mutate a gene with a given probability
        if random.random() < self.mutation_rate:
            index = random.randint(0, len(individual) - 1)
            individual[index] = random.choice(self.data)
        # Return the sorted individual
        return np.sort(individual)

    def genetic(self) -> list:
        """
        Main loop of the genetic algorithm. Performs genetic operations over multiple generations
        to find the optimal solution.

        Returns:
        np.ndarray: The best individual found after all generations.
        """
        # Iterate over multiple generations
        for _ in range(self.epoch_count):
            new_population = []
            for _ in range(self.population_size // 2):
                # Select parents and create children
                parent1 = self.tournament_selection()
                parent2 = self.tournament_selection()
                child1 = self.crossover(parent1, parent2)
                child2 = self.crossover(parent1, parent2)
                # Mutate children and add to new population
                new_population.extend([self.mutate(child1), self.mutate(child2)])
            # Update population
            self.population = new_population

        # Find and return the best individual based on fitness
        best_individual = min([list(item) for item in self.population], key=self.fitness)
        return best_individual
