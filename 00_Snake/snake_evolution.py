# -*- codingng: utf-8 -*-
"""
Created on Fri Apr 30 10:39:58 2021

@author: utente
"""

from call_snake import Population
from snake_crossover import arithmetic_co
from snake_mutation import geometric_mutation, normal_distribution_mutation
from snake_selection import fps, tournament, ranking

snakes = Population(size = 2, 
                    moves_till_stuck= 75)

snakes.evolve(  gens = 50, #Number of generations to be produced
                select = tournament, #Selection function
                crossover = arithmetic_co, #Crossover function
                mutate = geometric_mutation, #Mutation function
                co_p = 1, #crossover probability
                mu_p = 1, #mutation probability
                constant_ms = 7, #Geometric Mutation coefficient 
                tournament_size = 1,
                elitism = True, #wheter to perform elitisim
                record_diversity = False, #wheter to record diversity
                fitness_sharing = True)